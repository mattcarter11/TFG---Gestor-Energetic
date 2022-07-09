import time
import datetime as dt
from enum import Enum
from drivers.DataBase.InfluxDB import InfluxDB
from drivers.Load.LoadBase import LoadBase
from drivers.Load.Shelly import ShellyLoad
from drivers.PowerMeter.EnvoyS import EnvoyS

class AlgorithmsEnum(Enum):
    none = 0
    hysteresis = 1
    min_on_time = 2
    time_to_consume = 3

class PredictFinalEnergy(Enum):
    disabled = 0
    avarage_power = 1
    project_current_power = 2

# ======== Settings ========
# Global parameters
Ts              = 10 # [s]
database        = InfluxDB('10.10.10.100', 18086, 'gestor-energetic-SVC')
load1           = ShellyLoad('192.168.100.131', value=700, on_time=3630) # None = no load
load2           = ShellyLoad('192.168.100.132', value=1000, on_time=3630) # None = no load
powermeter      = EnvoyS('http://envoy.local/stream/meter', 'installer', 'aeceha39', 5, 20)
algorithm       = AlgorithmsEnum.time_to_consume
# Managing load interval
start_managing  = '06:00:00'
end_managing    = '23:59:59'
format_date     = '%H:%M:%S'

# Algorithms parameters
# Hysteresis thresholds [Wh]
th_top1         = 70
th_bottom1      = -10 
th_top2         = 200
th_bottom2      = 0
# Minimun On Time [s]
time_limit      = 600
# Time to Consume
predict         = PredictFinalEnergy.project_current_power
end_at_energy   = 0       # [Wh]
time_factor     = 1       # [0..1]
on_min_energy   = 75      # [Wh]  (must be > end_at_energy to avoid oscillations)

# Do not touch
on_min_energy = end_at_energy if end_at_energy > on_min_energy else on_min_energy
# ========== MAIN ==========
def is_load(load):
    return isinstance(load, LoadBase)

def next_hour_datetime(datetime:dt.datetime) -> dt.datetime:
    return datetime.replace(second=0, microsecond=0, minute=0) + dt.timedelta(hours=1)

def hystereis(load:LoadBase, th_top:float, th_bottom:float, energy_b:float):
    if energy_b >= th_top and not load.get_status()['ison']:
        load.set_status(True)
    elif energy_b <= th_bottom and load.get_status()['ison']:
        load.set_status(False)

def _TTC_load_control_on(load:LoadBase, is_on:bool, energy1h:float, time_remaining:float, i):
    if load.value > 0 and not is_on and energy1h >= on_min_energy:
        time_to_use = energy1h / load.value * 3600 # [s] <- Wh/W = h
        if time_to_use >= (time_remaining*time_factor):
            load.set_status(True)
            return 1
    return 0

def _TTC_load_control_off(load:LoadBase, is_on:bool, energy_b:float, power_a:float, time_remaining:float, i):
    if load.value > 0 and is_on:
        energy1h_if_off = energy_b + (power_a + load.get_power()) * time_remaining / 3600
        if energy1h_if_off <= end_at_energy:
            load.set_status(False)

if __name__ == '__main__':
    #region -> [Init]
    current_hour = None
    two_load_system = is_load(load1) and is_load(load2)
    next_hour = next_hour_datetime(dt.datetime.now())
    start_managing = dt.datetime.strptime(start_managing, format_date).time()
    end_managing = dt.datetime.strptime(end_managing, format_date).time()
    # Get power_b from monitoring so if we restart, we don't lose all the balance previously calculated
    sec_from_oclock = (dt.datetime.now() - dt.datetime.now().replace(minute=0, second=0, microsecond=0)).total_seconds()
    last_from_oclock = database.query(f'select last(*) from hysteresis where time > now() - {int(sec_from_oclock)}s')
    if last_from_oclock != []:
        current_hour = dt.datetime.now().hour
        energy_b = last_from_oclock[0]['last_energyA']

    if is_load(load1): load1.set_status(False)
    if is_load(load2): load2.set_status(False)
    #endregion

    while True:
        start = time.time()

        timestamp = dt.datetime.now()
        working_hours = start_managing <= timestamp.time() <= end_managing
        if working_hours:
            if is_load(load1): ison1 = load1.get_status()['ison']
            if is_load(load2): ison2 = load2.get_status()['ison']

        #region -> Get Power/Calc Energy
        # See if hour has passed
        if current_hour != timestamp.hour:
            energy_b = 0
            current_hour = timestamp.hour
            next_hour = next_hour_datetime(timestamp)
            # Refresh loads when hour change while in working hours
            if working_hours and algorithm != AlgorithmsEnum.min_on_time:
                if is_load(load1): load1.set_status(ison1)
                if is_load(load2): load2.set_status(ison2)
        
        power_a = powermeter.power_available()
        energy_b = (power_a) * Ts / 3600 + energy_b
        #endregion

        # region -> Algorithms
        if working_hours: # [Day] Control loads - [Night] Don't controal loads
            if algorithm == AlgorithmsEnum.hysteresis:
                if is_load(load1): hystereis(load1, th_top1, th_bottom1, energy_b)
                if is_load(load2): hystereis(load2, th_top2, th_bottom2, energy_b)

            elif algorithm == AlgorithmsEnum.min_on_time:
                if two_load_system:
                    time_to_use = energy_b/(load1.value+load2.value) * 3600 # [s] <- Wh/W = h
                    if time_to_use >= time_limit:
                        load1.set_status(True, time_limit)
                        load2.set_status(True, time_limit)
                    else:
                        time_to_use1 = energy_b/load1.value * 3600 # [s] <- Wh/W = h
                        time_to_use2 = energy_b/load2.value * 3600 # [s] <- Wh/W = h
                        if time_to_use1 >= time_limit and time_to_use2 >= time_limit:
                            if time_to_use1 <= time_to_use2:
                                load1.set_status(True, time_limit)
                            else:
                                load2.set_status(True, time_limit)
                        elif time_to_use1 >= time_limit:
                            load1.set_status(True, time_limit)
                        elif time_to_use2 >= time_limit:
                            load2.set_status(True, time_limit)
                            
                else:
                    # Select first load that can be controlled
                    load = load1 if is_load(load1) else load2
                    if is_load(load):
                        time_to_use = energy_b / load.value * 3600 # [s] <- Wh/W = h
                        if time_to_use >= time_limit:
                            load.set_status(True, time_limit)

            elif algorithm == AlgorithmsEnum.time_to_consume:
                time_remaining = (next_hour - timestamp).total_seconds()

                if predict == PredictFinalEnergy.disabled:
                    energy1h = energy_b
                elif predict == PredictFinalEnergy.avarage_power:
                    avg = energy_b / (3600-time_remaining)
                    energy1h = avg*3600
                elif predict == PredictFinalEnergy.project_current_power:
                    energy1h = energy_b + time_remaining*(power_a)/3600

                if two_load_system: 
                    if not ison1 and not ison2:
                        _TTC_load_control_on(load1, ison1, energy1h, time_remaining, 1)
                    elif ison1 and not ison2:
                        on = _TTC_load_control_on(load2, ison2, energy1h, time_remaining, 2)
                        if not on: # means maybe less power
                            _TTC_load_control_off(load1, ison1, energy_b, power_a, time_remaining, 1)
                    elif ison1 and ison2:
                        _TTC_load_control_off(load2, ison2, energy_b, power_a, time_remaining, 2)
                    
                else: # One load system
                    load = load1 if is_load(load1) else load2
                    ison = ison1 if is_load(load1) else ison2
                    if not ison:
                        _TTC_load_control_on(load, ison, energy1h, time_remaining, 1)
                    elif ison:
                        _TTC_load_control_off(load, ison, energy_b, time_remaining, 1)


        #endregion

        #region -> Wait
        runtime = time.time()-start
        time.sleep(max(0, Ts-runtime))
        #endregion


