import sqlite3, json
from types import SimpleNamespace

with open('settings.json', 'r') as f:
    settings = json.load(f, object_hook=lambda d: SimpleNamespace(**d))

charge_on = 0
i = 0

with sqlite3.connect(settings.simulation.driver_db) as con:
    con.row_factory = sqlite3.Row # Return data in dict format
    cur = con.cursor()
    cur.execute(f"select * from power where type == 'generated' and timestamp > datetime('{settings.simulation.start_timestamp}', '+1 seconds') and timestamp <= datetime('{settings.simulation.end_timestamp}') order by timestamp asc")
    generated = cur.fetchall()
max_i = len(generated)

def get_generated() -> float:
    global g_prev_timestamp, i
    if i > max_i-1:
        return (None, None)
    data = generated[i]
    i += 1
    g_prev_timestamp = data['timestamp']
    return (data['value'], data['timestamp'])

def get_consumed() -> float:
    return charge_on*settings.charges.a.tdp_W + settings.simulation.base_tdp_W

def set_charge(value:bool):
    global charge_on
    charge_on = value

def get_charge() -> bool:
    return charge_on

if __name__ == "__main__":
    data = 0
    while data != (None, None):
        data = get_generated()
        print(data)