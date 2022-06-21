import pandas as pd
import numpy as np
import datetime as dt
from .constants import COL_ORDER

numType  = (float, np.float64, int, np.int64)

class DataFrameIn:

    def __init__(self, df:pd.DataFrame, _correct=True):
        if _correct:
            self._set_col_dtype()
            if not self._validate(df):
                raise Exception(f'DataFrame must have the colums {self.columns} with types {self.dtypes}')
            # df = df[self.columns].copy()

            mask = df['powerP'].values < 0
            if mask.any(): # Check is x10 times faster than directly doing the substiution
                df.loc[mask, "powerP"] = 0 # Fastest

            if df.isna().values.any(): # Check is x100 times faster than filling
                df = df.fillna(0)

        self.df = df
        self.Ts = self.calc_Ts()
        self.nsamples = len(df.index)
        self.nsec = self.nsamples*self.Ts

    def _set_col_dtype(self):
        self.columns = ['timestamp', 'powerP']
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
        self.columns = ['timestamp', 'powerP', 'powerC', 'powerL1', 'powerL2', 'on_offL1', 'on_offL2']
        self.dtypes = [dt.date, numType, numType, numType, numType, numType, numType]
        
    def _fill_missing_LB(self):
        if 'powerC' in self.df.columns and 'powerLB' not in self.df.columns:
            # x50..100 Faster vs normal iteration
            self.df['powerLB'] = self.df.loc[:,'powerC'].values - self.df.loc[:,'powerL1'].values - self.df.loc[:,'powerL2'].values
            self.df.loc[self.df['powerLB'].values < 0, 'powerLB'] = 0
    
    def fill_powerAG(self):
        self.df['powerA'] = self.df['powerP'].values - self.df['powerC'].values
        power_g = self.df['powerA'].copy()
        power_g[power_g.values > 0] = 0
        self.df['powerG'] = -power_g
        self.df.loc[self.df['powerA'].values < 0, 'powerA'] = 0 # Fastest
        self.df['powerGP'] = self.df['powerG'].copy()
        self.df.loc[self.df['powerP'].values <= 0, 'powerGP'] = 0 # Fastest

    def split_energyB(self):
        self.df['energyAB'] = self.df['energyB'].copy()
        self.df.loc[self.df['energyAB'].values < 0, 'energyAB']= 0 # Fastest
        self.df['energyGD'] = -self.df['energyB'].copy()
        self.df.loc[self.df['energyGD'].values < 0, 'energyGD']= 0 # Fastest

    def fill_missing_energy(self):
        calcB = 'energyB' not in self.df.columns or self.df['energyB'].isna().any()
        calcP = 'energyP' not in self.df.columns or self.df['energyP'].isna().any()
        if calcB or calcP:
            energyB, energyP = [], []
            current_hour = None
            for row in self.df.to_dict('records'):  #x5..10 Faster vs .iterrows()
                hourstamp   = row['timestamp'].hour
                power_g     = row['powerP']

                if current_hour != hourstamp:
                    energy_b = energy_p =  0
                    current_hour = hourstamp

                if calcB: 
                    power_c     = row['powerLB'] + row['powerL1'] + row['powerL2']
                    energy_b = (power_g - power_c) * self.Ts / 3600 + energy_b
                    energyB.append( energy_b )

                if calcP:
                    energy_p = (power_g * self.Ts) / 3600 + energy_p
                    energyP.append( energy_p )

            if calcB: 
                self.df['energyB'] = energyB
            if calcP: 
                self.df['energyP'] = energyP
        if any([x not in self.df.columns for x in ['energyAB', 'energyGD']]):
            self.split_energyB() 
        