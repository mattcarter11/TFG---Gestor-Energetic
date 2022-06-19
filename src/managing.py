import time
import datetime as dt
from enum import Enum
from drivers.DataBase.InfluxDB import InfluxDB
from drivers.Load.LoadBase import LoadBase
from drivers.Load.Shelly import ShellyLoad
from drivers.PowerMeter.JordiPM import JordiPM

class AlgorithmsEnum(Enum):
    hysteresis = 1
    min_on_time = 2
    time_to_consume = 3

class PredictFinalEnergy(Enum):
    disabled = 0
    avarage_power = 1
    project_current_power = 2

# ======== INIT ========
# Global parameters
Ts              = 10 # [s]
database        = InfluxDB('10.10.10.100', 18086, 'gestor-energetic-SVC')
load1           = ShellyLoad('192.168.100.131', value=700, on_time=3630) # None = no load
load2           = ShellyLoad('192.168.100.132', value=1000, on_time=3630) # None = no load
powermeter      = JordiPM('http://envoy.local/stream/meter', 'installer', 'aeceha39', 5, 20)
algorithm       = AlgorithmsEnum.time_to_consume
# Managing load interval
start_managing  = '06:00:00'
end_managing    = '23:59:59'
format_date     = '%H:%M:%S'

# Algorithms parameters
# Hysteresis thresholds [Wh]
th_top1         = 100
th_bottom1      = -10 
th_top2         = 170
th_bottom2      = 100
# Minimun On Time [s]
time_limit      = 600
# Time to Consume
predict         = PredictFinalEnergy.project_current_power
on_min_energy   = 10        # [Wh]
time_factor     = 0.9       # [0..1]
end_at_energy   = 150       # [Wh]

# ======== MAIN ========
def is_load(load):
    return isinstance(load, LoadBase)

def next_hour_datetime(datetime:dt.datetime) -> dt.datetime:
    return datetime.replace(second=0, microsecond=0, minute=0) + dt.timedelta(hours=1)

def hystereis(load:LoadBase, is_on, th_top:float, th_bottom:float, energy_a:float):
    if energy_a >= th_top and not is_on:
        load.set_status(True)
    elif energy_a <= th_bottom and is_on:
        load.set_status(False)

def _TTC_load_control_on(load:LoadBase, is_on:bool, energy_a:float, time_remaining:float, i):
    if predict == PredictFinalEnergy.disabled:
        energy1h = energy_a
    elif predict == PredictFinalEnergy.avarage_power:
        avg = energy_a / (3600-time_remaining)
        energy1h = avg*3600
    elif predict == PredictFinalEnergy.project_current_power:
        energy1h = energy_a + time_remaining*(powermeter.power_available())/3600

    print(f'[{i}]  On:{is_on:1}  e1h: {energy1h:<7.2f}')
    if load.value > 0 and not is_on and energy1h >= on_min_energy:
        time_to_use = energy1h / load.value * 3600 # [s] <- Wh/W = h
        if time_to_use >= (time_remaining*time_factor):
            load.set_status(True)

def _TTC_load_control_off(load:LoadBase, is_on:bool, energy_a:float, power_a:float, time_remaining:float, i):
    print(f'[{i}]  On:{is_on:1}  eA: {energy_a:<7.2f}  pA: {power_a:<7.2f}')
    if load.value > 0 and is_on:
        energy1h_if_off = energy_a + (power_a + load.get_power()) * time_remaining / 3600
        if energy1h_if_off <= end_at_energy:
            load.set_status(False)

if __name__ == '__main__':
    # Get power_a from monitoring so they can start synced, plus it makes all that hour slot more efficient
    last60s = database.query('select last(*) from hysteresis where time > now() - 60s')
    energy_a = last60s[0]['last_energyA'] if last60s else 0
    current_hour = dt.datetime.now().hour
    next_hour = next_hour_datetime(dt.datetime.now())
    start_managing = dt.datetime.strptime(start_managing, format_date).time()
    end_managing = dt.datetime.strptime(end_managing, format_date).time()

    if is_load(load1): load1.set_status(False)
    if is_load(load2): load2.set_status(False)

    while True:
        start = time.time()

        #region -> Get load data
        if is_load(load1): l1 = load1.get_status()
        if is_load(load2): l2 = load2.get_status()
        #endregion

        #region -> Power
        # See if hour has passed
        timestamp = dt.datetime.now()
        working_hours = start_managing <= timestamp.time() <= end_managing
        if current_hour != timestamp.hour:
            energy_a = 0
            current_hour = timestamp.hour
            next_hour = next_hour_datetime(timestamp)
            if working_hours: # Refresh loads when hour change in working hours
                if is_load(load1): load1.set_status(l1['ison'])
                if is_load(load2): load2.set_status(l2['ison'])
        
        power_g, power_c = powermeter.power_gc()
        power_a = power_g - power_c
        energy_a = (power_a) * Ts / 3600 + energy_a
        #endregion

        # region -> Algorithms
        if working_hours: # [Day] Control loads - [Night] Don't controal loads
            if algorithm == AlgorithmsEnum.hysteresis:
                if is_load(load1): hystereis(load1, l1['ison'], th_top1, th_bottom1, energy_a)
                if is_load(load2): hystereis(load2, l2['ison'], th_top2, th_bottom2, energy_a)

            elif algorithm == AlgorithmsEnum.min_on_time:
                # Select first load that can be controlled
                load = load1 if is_load(load1) else load2 if is_load(load2) else None
                lX = l1 if is_load(load1) else l2 if is_load(load2) else None
                if is_load(load):
                    time_to_use = energy_a / load.value * 3600 # [s] <- Wh/W = h
                    if time_to_use >= time_limit:
                        load.set_status(True, time_limit)

            elif algorithm == AlgorithmsEnum.time_to_consume:
                time_remaining = (next_hour - timestamp).total_seconds()
                print(f'\n[{timestamp}] left: {time_remaining}s')
                if is_load(load1): _TTC_load_control_on(load1, l1['ison'], energy_a, time_remaining, 1)
                if is_load(load2): _TTC_load_control_on(load2, l2['ison'], energy_a, time_remaining, 2)
                if is_load(load2): _TTC_load_control_off(load2, load2.get_status()['ison'], energy_a, powermeter.power_available(), time_remaining, 2)
                if is_load(load1): _TTC_load_control_off(load1, load1.get_status()['ison'], energy_a, powermeter.power_available(), time_remaining, 1)
        #endregion

        # Wait
        runtime = time.time() - start
        time.sleep(max(0, Ts - runtime))


