import sqlite3, time
import datetime as dt
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def icsv2sqlite(csv_file, db_file, timestamp_format = "%Y-%m-%dT%H:%M:%S%z"):
    """
    Info:
        - CSV file format: timestamp,power,entry_type \n
            - timestamp: %Y-%m-%dT%H:%M:%S%z
            - power: float
            - entry_type: generated or consumed
    """
    with sqlite3.connect(db_file) as con: # Auto commints changes and closes connection
        cur = con.cursor()

        # Regenerate table (remove old, add new)
        cur.execute('drop table if exists power')
        cur.execute('''
            create table power (
                timestamp timestamp not null,
                type text not null check((type='generated') or (type='consumed')),
                value real not null
            )
        ''')

        # Clear the csv to have time, value, type and insert
        with open(csv_file, 'r') as f:
            for l in f:
                l = l.strip().split(',')
                datetime = dt.datetime.strptime(l[0], timestamp_format)
                cur.execute(f"insert into power values ('{datetime}', '{l[2]}', {l[1]})")

def plot_power(db, start_date = None, end_date = None):
    """ Date format: "%Y-%m-%d %H:%M:%S%z """
    data = db_select(db, 'power', start_date, end_date)
    
    dic = {"consumed": {"x":[], "y":[], "color":"orange"}, "generated": {"x":[], "y":[], "color":"green"}}

    # Power consumed
    data = db_select(db, 'power', start_date, end_date, "type == 'consumed'")
    print(f'Power Consumed -> {len(data)}')
    plt.plot(data.timestamp, data.value, '-', color="orange", label="power consumed")
    # Power generated
    data = db_select(db, 'power', start_date, end_date, "type == 'generated'")
    print(f'Power Generated -> {len(data)}')
    plt.plot(data.timestamp, data.value, '-', color="green", label="power generated")


def align_yaxis_np(ax1, ax2):
    """Align zeros of the two axes, zooming them out by same ratio"""
    axes = np.array([ax1, ax2])
    extrema = np.array([ax.get_ylim() for ax in axes])
    tops = extrema[:,1] / (extrema[:,1] - extrema[:,0])
    # Ensure that plots (intervals) are ordered bottom to top:
    if tops[0] > tops[1]:
        axes, extrema, tops = [a[::-1] for a in (axes, extrema, tops)]

    # How much would the plot overflow if we kept current zoom levels?
    tot_span = tops[1] + 1 - tops[0]

    extrema[0,1] = extrema[0,0] + tot_span * (extrema[0,1] - extrema[0,0])
    extrema[1,0] = extrema[1,1] + tot_span * (extrema[1,0] - extrema[1,1])
    [axes[i].set_ylim(*extrema[i]) for i in range(2)]

def db_cmd_append_condition(cmd, condition):
    cmd = cmd + " and " if 'where' in cmd else cmd + " where "
    cmd += condition
    return cmd

def db_select(db, table, select, start_date = None, end_date = None, condition = None, group = None):
    with sqlite3.connect(db) as con: # Auto commints changes and closes connection
        cmd = f"select {select} from {table}"
        if start_date != None:
            cmd = db_cmd_append_condition(cmd, f"where timestamp >= datetime('{start_date}')")
        if end_date != None:
            cmd = db_cmd_append_condition(cmd, f"timestamp <= datetime('{end_date}')")
        if condition != None:
            cmd = db_cmd_append_condition(cmd, condition)
        if group != None:
            cmd += ' group by '+ group
        data = pd.read_sql_query(cmd, con, parse_dates=['timestamp'])
    return data

def plot_sim(db, start_date = None, end_date = None, title = ''):
    """ Date format: "%Y-%m-%d %H:%M:%S%z """

    fig, axs = plt.subplots()
    # ==== Line Plots ====
    ax1 = axs
    ax2 = ax1.twinx()
    ax1.set_xlabel('Dat & Time')
    ax1.set_ylabel('Power [W]')
    ax2.set_ylabel('Energy [kJ]')
    ax1.grid(True, linestyle=':')
    ax1.set_title(title)
    
    # Power Consumed
    data = db_select(db, 'power', '*', start_date, end_date, "type == 'consumed'")
    print(f'Power Consumed -> {len(data)}')
    ax1.plot(data.timestamp, data.value, '-', color="orange", label="Power Consumed")
    # Power Generated
    data = db_select(db, 'power', '*', start_date, end_date, "type == 'generated'")
    print(f'Power Generated -> {len(data)}')
    ax1.plot(data.timestamp, data.value, '-', color="green", label="Power Generated")
    # Energy Available
    data = db_select(db, 'energy', '*', start_date, end_date, "type == 'available'")
    print(f'Energy -> {len(data)}')
    ax2.plot(data.timestamp, data.value, '-', color="blue", label="Available Energy")
    # Energy Total
    # data = db_select(db, 'energy', '*', start_date, end_date, "type == 'total'")
    # print(f'Energy -> {len(data)}')
    # ax2.plot(data.timestamp, data.value, '-', color="dodgerblue", label="Total Energy", alpha=0.5)

    ax1.legend(loc="upper left")
    ax2.legend(loc="upper right")
    align_yaxis_np(ax1, ax2)


    # ==== Energy Loss ====
    fig, ax = plt.subplots()
    energy_l = db_select(db, 'energy', 'max(timestamp) timestamp, value', start_date, end_date, "type == 'available'", group = "strftime ('%H',timestamp)")
    energy_t = db_select(db, 'energy', 'max(timestamp) timestamp, value', start_date, end_date, "type == 'total'", group = "strftime ('%H',timestamp)")
    ax.bar(energy_t.timestamp, energy_t.value, color="green", label="Energy Used", width =0.01)
    ax.bar(energy_l.timestamp, energy_l.value, color="orange", label="Energy Lost", width =0.01)

    ax.legend(loc="upper left")
    ax.grid(True, linestyle=':')
    ax.set_xlabel('Dat & Time')
    ax.set_ylabel('Energy [kJ]')
    ax.set_title(title)

    plt.show()


if __name__ == "__main__":
    start = time.time()

    # icsv2sqlite('src/influxdb.csv', 'db/power.db')
    # icsv2sqlite('src/influxdb2.csv', 'db/power2.db')
    # plot_power('db/power2.db')
    plot_sim('db/simulation.db')

    print(f'Execution Time -> {time.time() - start}')
