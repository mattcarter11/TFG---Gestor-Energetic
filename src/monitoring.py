import time
import datetime as dt
from drivers.DataBase.InfluxDB import InfluxDB
from drivers.Load.LoadBase import LoadBase
from drivers.Load.Shelly import ShellyLoad
from drivers.PowerMeter.JordiPM import JordiPM

# ======== Settings ========
Ts          = 10
database    = InfluxDB('10.10.10.100', 18086, 'gestor-energetic-SVC')
table       = 'hysteresis'
load1       = ShellyLoad('192.168.100.131')     # None = no load
load2       = ShellyLoad('192.168.100.132')     # None = no load
powermeter  = JordiPM('http://envoy.local/stream/meter', 'installer', 'aeceha39', 5, 20)

# ========== MAIN ==========
def is_load(load):
    return isinstance(load, LoadBase)
    
if __name__ == '__main__':
    current_hour = prel1 = prel2 = None
    while True:
        start = time.time()

        #region -> Power
        # See if hour has passed
        timestamp = dt.datetime.now()
        if current_hour != timestamp.hour:
            energy_a = energy_p = 0
            current_hour = timestamp.hour
        
        power_g, power_c = powermeter.power_gc()
        energy_a = (power_g-power_c) * Ts / 3600 + energy_a
        energy_p = power_g*Ts / 3600 + energy_p
        #endregion

        #region -> Load (on/off & power)
        if is_load(load1):
            l1 = load1.get_status()
            on_off_l1 = 1 if not prel1 and l1['ison'] else -1 if prel1 and not l1['ison'] else 0
            prel1 = l1['ison']
        if is_load(load2):
            l2 = load2.get_status()
            on_off_l2 = 1 if not prel2 and l2['ison'] else -1 if prel2 and not l2['ison'] else 0
            prel2 = l2['ison']
        #endregion

        #region -> Store data
        dic = {
            "powerG": power_g,
            "powerC": power_c,
            "energyA": energy_a,
            "energyP": energy_p,
            "on_offL1": on_off_l1 if is_load(load1) else None,
            "on_offL2": on_off_l2 if is_load(load2) else None,
            "powerL1": l1['power'] if is_load(load1) else None,
            "powerL2": l2['power'] if is_load(load2) else None,
        }
        database.insert(table, dic)
        #endregion

        # Wait
        runtime = time.time()-start
        time.sleep(max(0, Ts-runtime))

