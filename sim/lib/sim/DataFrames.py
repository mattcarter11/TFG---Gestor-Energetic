import pandas as pd
import numpy as np
import datetime as dt
from time import time_ns, time

numType  = (float, np.float64, int, np.int64)
COL_ORDER =[ 
    'timestamp',
    'powerG', 'powerC', 'powerLB', 'powerL1', 'powerL2',
    'on_offL1', 'on_offL2', 
    'energySY', 'energyP',  'energyG',
    'energyC', 'energyLB', 'energyL1', 'energyL2',
    'energyA', 'energyS', 'energyL',
    'energyCM', 
    ]

class DataFrameIn:

    def __init__(self, df:pd.DataFrame, _correct=True):
        if _correct:
            self._set_col_dtype()
            if not self._validate(df):
                raise Exception(f'DataFrame must have the colums {self.columns} with types {self.dtypes}')
            # df = df[self.columns].copy()

            mask = df['powerG'].values < 0
            if mask.any(): # Check is x10 times faster than directly doing the substiution
                df.loc[mask, "powerG"] = 0 # Fastest

            if df.isna().values.any(): # Check is x100 times faster than filling
                df = df.fillna(0)

        self.df = df
        self.Ts = self.calc_Ts()
        self.nsamples = len(df.index)
        self.nsec = self.nsamples*self.Ts

    def _set_col_dtype(self):
        self.columns = ['timestamp', 'powerG']
        self.dtypes = [dt.date, numType]

    def _validate(self, df:pd.DataFrame) -> bool:
        if all([x in df.columns for x in self.columns]):
            if all([isinstance(df[col].iloc[0], self.dtypes[i]) for i, col in enumerate(self.columns)]):
                    return True
        return False
    
    def rearange_cols(self):
        columns = [col for col in COL_ORDER if col in self.df.columns]
        self.df = self.df[columns]
       
    def calc_Ts(self):
        return round( (self.df['timestamp'].iloc[2] - self.df['timestamp'].iloc[1]).total_seconds() )

    def split_energyA(self):
        energy_g = self.df['energyA'].copy()
        energy_g[energy_g.values > 0] = 0
        self.df['energyG'] = -energy_g
        self.df.loc[self.df['energyA'].values < 0, 'energyA'] = 0 # Fastest

    def select_daterange(self, start:str, end:str, min_sec:int=300):
        if self.nsamples <= (min_sec/self.Ts):
            raise Exception(self, "Error", f"Date & Time interval must be at least {min_sec} s")

        df = self.df[self.df['timestamp'].between(start, end)].copy()
        if isinstance(self, DataFrameOut):
            return DataFrameOut(df, False)
        return DataFrameIn(df, False)

class DataFrameOut (DataFrameIn):

    def __init__(self, df:pd.DataFrame, _correct=True):
        super().__init__(df, _correct)
        self._fill_missing_LB()

    def _set_col_dtype(self):
        self.columns = ['timestamp', 'powerG', 'powerC', 'powerL1', 'powerL2', 'on_offL1', 'on_offL2']
        self.dtypes = [dt.date, numType, numType, numType, numType, numType, numType]
        
    def _fill_missing_LB(self):
        if 'powerC' in self.df.columns and 'powerLB' not in self.df.columns:
            # x50..100 Faster vs normal iteration
            self.df['powerLB'] = self.df.loc[:,'powerC'].values - self.df.loc[:,'powerL1'].values - self.df.loc[:,'powerL2'].values
            self.df.loc[self.df['powerLB'].values < 0, 'powerLB'] = 0

    def fill_missing_power(self):
        if any([column not in self.df.columns or self.df[column].isna().any() for column in ['energyA', 'energyP']]):
            energyA = []
            energyP = []
            current_hour = None
            for row in self.df.to_dict('records'):  #x5..10 Faster vs .iterrows()
                timestamp   = row['timestamp']
                power_g     = row['powerG']
                power_c     = row['powerLB'] + row['powerL1'] + row['powerL2']

                if current_hour != timestamp.hour:
                    energy_a = energy_p =  0
                    current_hour = timestamp.hour

                energy_a = (power_g - power_c) * self.Ts / 3600 + energy_a
                energy_p = (power_g * self.Ts) / 3600 + energy_p
                energyA.append( energy_a )
                energyP.append( energy_p )

            if 'energyA' not in self.df.columns or self.df['energyA'].isna().any():
                self.df['energyA'] = energyA
            if 'energyP' not in self.df.columns or self.df['energyP'].isna().any():
                self.df['energyP'] = energyP        

        if 'energyG' not in self.df.columns or self.df['energyG'].isna().any():
            self.split_energyA()
