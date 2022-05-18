import sqlite3, json, driver, tools
import datetime as dt
from types import SimpleNamespace

# ======== INIT ========
# Load settings
with open('settings.json', 'r') as f:
    settings = json.load(f, object_hook=lambda d: SimpleNamespace(**d))

# Simulation DB results
with sqlite3.connect(settings.simulation.db) as con: # Auto commints changes and closes connection
    cur = con.cursor()

    if settings.simulation.clean_db:
        cur.execute('drop table if exists energy')
        cur.execute('drop table if exists power')

    # Create table if missing
    cur.execute('''
        create table if not exists energy (
            timestamp timestamp not null,
            type text not null check((type='total') or (type='available')),
            value real not null
        )
    ''')
    cur.execute('''
        create table if not exists power (
            timestamp timestamp not null,
            type text not null check((type='generated') or (type='consumed')),
            value real not null
        )
    ''')

# ======== MAIN ========
current_hour = None
while True:
    # Get current power
    power_g, timestamp = driver.get_generated()
    if power_g == None: # End of database == End of simulation
        break
    timestamp = dt.datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S%z")
    power_c = driver.get_consumed()

    # See if hour has passed
    if current_hour != timestamp.hour:
        print('energy reset', current_hour, timestamp.hour)
        energy_t = energy_a = 0
        current_hour = timestamp.hour
        next_hour = timestamp.replace(second=0, microsecond=0, minute=0) + dt.timedelta(hours=1)


    # Calc acomulated energy
    energy_t = (power_g * settings.sampling_s)/1000 + energy_t
    energy_a = ((power_g - power_c) * settings.sampling_s)/1000 + energy_a

    # Algorithm
    match settings.algorithm:
        case "Hysteresis":
            if energy_a >= settings.threshold.top_kJ:
                driver.set_charge(True)
            elif energy_a <= settings.threshold.bottom_kJ:
                driver.set_charge(False)

        case "time_to_use":
            time_remaining = (next_hour - timestamp).total_seconds()
            time_to_use = energy_a*1000/settings.charges.a.tdp_W
            if time_to_use >= time_remaining:
                driver.set_charge(True)
            elif energy_a <= 0:
                driver.set_charge(False)

        case "time_to_use_predict":
            time_remaining = (next_hour - timestamp).total_seconds()
            energy_p = energy_a*1000 + time_remaining*power_g
            time_to_use = energy_p/settings.charges.a.tdp_W
            if time_to_use >= time_remaining:
                driver.set_charge(True)
            elif energy_p <= 0:
                driver.set_charge(False)

    # Store energy and power to plot simulation
    with sqlite3.connect(settings.simulation.db) as con:
        cur = con.cursor()
        cur.execute(f"insert into energy values ('{timestamp}', 'total', {energy_t}), ('{timestamp}', 'available', {energy_a})")
        cur.execute(f"insert into power values ('{timestamp}', 'generated', {power_g}), ('{timestamp}', 'consumed', {power_c})")

# Plot if simulating
title = f'{settings.algorithm.replace("_", " ").title()}'
match settings.algorithm:
    case "hysteresis":
        title += f' -> Top: {settings.threshold.top_kJ} kJ Bottom: {settings.threshold.bottom_kJ} kJ  |  TDP -> base: {settings.simulation.base_tdp_W} W  c1: {settings.charges.a.tdp_W} W | DB: {settings.simulation.driver_db}\n'
    case "time_to_use" | "time_to_use_predict":
        title += f'  |  TDP -> base: {settings.simulation.base_tdp_W} W  c1: {settings.charges.a.tdp_W} W | DB: {settings.simulation.driver_db}\n'
    
tools.plot_sim(settings.simulation.db, title = title)

