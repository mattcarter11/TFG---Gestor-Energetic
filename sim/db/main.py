from importlib.metadata import files
from numpy import int64
import pandas as pd
import datetime as dt

def G_merge_LB(fileG, fileLB, fileSave):
    df1 = pd.read_csv(fileG, parse_dates=['timestamp'])
    df2 = pd.read_csv(fileLB, parse_dates=['timestamp'])

    df1['powerLB'] = df2['powerLB']
    df1.to_csv(fileSave, index=False)

def process_paco(fileOpen, fileSave):
    df = pd.read_csv(fileOpen, parse_dates=['_time'])
    df = df[df['_field'] == 'PAC']
    df = df[['_time', '_value']]
    df.rename(columns={'_time': 'timestamp', '_value': 'powerP'}, inplace=True, errors='raise')
    df.to_csv(fileSave, index=False)


def jordi_open(fileOpen):
    # Load
    df = pd.read_csv(fileOpen, parse_dates=['time'])
    # Remove/renamve columns
    df.drop(['name'], axis = 1, inplace = True)
    df.rename(columns={'time': 'timestamp','powerG': 'powerP', 'energyA':'energyB'}, inplace=True, errors='raise')
    # Format datetime
    df['timestamp'] = pd.to_datetime(df['timestamp'].astype('int64'))
    # Add powerA
    df['powerA'] = df['powerP'].values - df['powerC'].values
    return df

def proces_jordi(df:pd.DataFrame, fileSave:str, start:str, end:str):
    # Grab range
    start_mask = dt.datetime.strptime(start, "%Y-%m-%d")
    end_mask = dt.datetime.strptime(end, "%Y-%m-%d")
    mask = (df['timestamp'] > start_mask) & (df['timestamp'] <= end_mask)
    df = df.loc[mask]
    # mask = (20 <= df['timestamp'].dt.hour) | (df['timestamp'].dt.hour <= 2)
    # df.loc[mask, 'powerC'] = 150
    # df.loc[mask, ['powerL1', 'powerL2']] = 0
    df.to_csv(f'{start}..{end} {fileSave}', index=False)

if __name__ == "__main__":
    # G_merge_LB('2022-02-1..8 (G).csv', 'consumed.csv', '2022-02-1..8 (G+LB).csv')
    # process_paco('2022-03-11..13.csv', '2022-03-11..13 Pluja (G).csv')
    df = jordi_open('hysteresis.csv')
    # proces_jordi(df, 'Jordi.csv', "2022-04-22", "2022-04-27")
    # proces_jordi(df, 'Jordi.csv', "2022-04-27", "2022-05-02")
    proces_jordi(df, 'Jordi.csv', "2022-05-02", "2022-05-08")
    # proces_jordi(df, 'Jordi.csv', "2022-05-08", "2022-05-13")
    # proces_jordi(df, 'Jordi.csv', "2022-05-17", "2022-05-22")
    # proces_jordi(df, 'Jordi.csv', "2022-05-22", "2022-05-27")
    # proces_jordi(df, 'Jordi.csv', "2022-05-27", "2022-06-01")
    # proces_jordi(df, 'Jordi.csv', "2022-06-01", "2022-06-06")
    # proces_jordi(df, 'Jordi.csv', "2022-06-06", "2022-06-11")
    # proces_jordi(df, 'Jordi.csv', "2022-06-11", "2022-06-14")
    # proces_jordi(df, 'Jordi.csv', "2022-04-22", "2022-06-14") # All

