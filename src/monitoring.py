import time
import datetime as dt
from drivers.DataBase.InfluxDB import InfluxDB
from drivers.Load.LoadBase import LoadBase
from drivers.Load.Shelly import ShellyLoad
from drivers.PowerMeter.EnvoyS import EnvoyS

# ======== Settings ========
Ts          = 10
database    = InfluxDB('10.10.10.100', 18086, 'gestor-energetic-SVC')
table       = 'hysteresis'
load1       = ShellyLoad('192.168.100.131')     # None = no load
load2       = ShellyLoad('192.168.100.132')     # None = no load
powermeter  = EnvoyS('http://envoy.local/stream/meter', 'installer', 'aeceha39', 5, 20)

# ========== MAIN ==========
def is_load(load):
    return isinstance(load, LoadBase)
    
if __name__ == '__main__':
    #region -> Init
    current_hour = prel1 = prel2 = None
    # Get data from last same inside the hour slot
    sec_from_oclock = (dt.datetime.now() - dt.datetime.now().replace(minute=0, second=0, microsecond=0)).total_seconds()
    last_from_oclock = database.query(f'select last(*) from hysteresis where time > now() - {int(sec_from_oclock)}s')
    if last_from_oclock != []:
        current_hour = dt.datetime.now().hour
        energy_b = last_from_oclock[0]['last_energyA']
        energy_p = last_from_oclock[0]['last_energyP']
        prel1 = bool(last_from_oclock[0]['last_on_offL1'])
        prel2 = bool(last_from_oclock[0]['last_on_offL2'])
    #endregion

    while True:
        start = time.time()

        #region -> Get Power/Calc Energy
        # See if hour has passed
        timestamp = dt.datetime.now()
        if current_hour != timestamp.hour:
            energy_b = energy_p = 0
            current_hour = timestamp.hour
        
        power_p, power_c = powermeter.power_pc()
        energy_b = (power_p-power_c) * Ts / 3600 + energy_b
        energy_p = power_p*Ts / 3600 + energy_p
        #endregion

        #region -> Get Loads (on/off & power)
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
            "powerP": power_p,
            "powerC": power_c,
            "energyB": energy_b,
            "energyP": energy_p,
            "on_offL1": on_off_l1 if is_load(load1) else None,
            "on_offL2": on_off_l2 if is_load(load2) else None,
            "powerL1": l1['power'] if is_load(load1) else None,
            "powerL2": l2['power'] if is_load(load2) else None,
        }
        database.insert(table, dic)
        #endregion

        #region -> Wait
        runtime = time.time()-start
        time.sleep(max(0, Ts-runtime))
        #endregion
