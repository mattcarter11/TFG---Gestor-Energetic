import time
import datetime as dt
from enum import Enum
from drivers.Load.Load import Load
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
load1           = ShellyLoad('192.168.100.131', value=700) # None = no load
load2           = ShellyLoad('192.168.100.132', value=700) # None = no load
powermeter      = JordiPM('http://envoy.local/stream/meter', 'installer', 'aeceha39', 5, 20)
algorithm       = AlgorithmsEnum.hysteresis
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
time_factor     = 0.75      # [0..1]
end_at_energy   = 100       # [Wh]

# ======== MAIN ========
current_hour = None
start_managing = dt.datetime.strptime(start_managing, format_date).time()
end_managing = dt.datetime.strptime(end_managing, format_date).time()

def is_load(load):
    return isinstance(load, Load)

def _TTC_load_control(load:Load, energy_a:float, power_a:float, energy1h:float, time_remaining:float, algorithm):
    if load.power > 0:
        if not load.on:
            if energy1h >= on_min_energy:
                time_to_use = energy1h / load.power * 3600 # [s] <- Wh/W = h
                if time_to_use >= (time_remaining*time_factor):
                    load.set_status(True)
        else:
            energy1h_if_off = energy_a + (power_a + load.get_power()) * time_remaining / 3600
            if energy1h_if_off <= end_at_energy:
                load.set_status(False)

if __name__ == '__main__':
    load1.set_status(False)
    load2.set_status(False)

    while True:
        start = time.time()

        #region -> Get load data
        if is_load(load1):
            l1 = load1.get_status()
        if is_load(load1):
            l2 = load2.get_status()
        #endregion

        #region -> Power
        # See if hour has passed
        timestamp = dt.datetime.now()
        working_hours = start_managing <= timestamp.time() <= end_managing
        if current_hour != timestamp.hour:
            energy_a = 0
            current_hour = timestamp.hour
            next_hour = timestamp.replace(second=0, microsecond=0, minute=0) + dt.timedelta(hours=1)
            if working_hours: # Refresh loads when hour change in working hours
                load1.set_status(l1['ison'])
                load2.set_status(l2['ison'])
        
        power_g, power_c = powermeter.power_gc()
        energy_a = (power_g-power_c) * Ts / 3600 + energy_a
        #endregion

        # region -> Algorithms
        if working_hours: # [Day] Control loads - [Night] Don't controal loads
            if algorithm == AlgorithmsEnum.hysteresis:
                if is_load(load1):
                    if energy_a >= th_top1 and not l1['ison']:
                        load1.set_status(True, 3630)
                    elif energy_a <= th_bottom1 and l1['ison']:
                        load1.set_status(False)
                if is_load(load2):
                    if energy_a >= th_top2 and not l2['ison']:
                        load2.set_status(True, 3630)
                    elif energy_a <= th_bottom2 and l2['ison']:
                        load2.set_status(False)

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

                if predict == PredictFinalEnergy.disabled:
                    energy1h = energy_a
                elif predict == PredictFinalEnergy.avarage_power:
                    avg = energy_a / (3600-time_remaining)
                    energy1h = avg*3600
                elif predict == PredictFinalEnergy.project_current_power:
                    energy1h = energy_a + time_remaining*(power_a)/3600

                on_offL1 = _TTC_load_control(load1, energy_a, power_a, energy1h, time_remaining, algorithm)

                energy1h = energy1h - load1.get_power() * time_remaining / 3600
                power_a = power_a + load1.get_power()
                on_offL2 = _TTC_load_control(load2, energy_a, power_a, energy1h, time_remaining, algorithm)
        #endregion

        # Wait
        runtime = time.time() - start
        time.sleep(max(0, Ts - runtime))


