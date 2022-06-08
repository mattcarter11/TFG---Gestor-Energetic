import pandas as pd
import numpy as np
from .DataFrames import DataFrameOut 

class Results:

    def __init__(self, df:DataFrameOut, df_price=None, sell_price:float|int=0.1):
        df.fill_missing_power()
        self.Ts = df.Ts
        self.nsec = df.nsec
        self.df_in = df.df.copy()
        self.sim_hours = self.nsec/3600
        self.sim_days = 24/self.sim_hours
        self.df_price = df_price
        self.sell_price = sell_price
        self.df_hour = pd.DataFrame()
        self.df_total = pd.DataFrame()
        self.df_results = pd.DataFrame()
        self._hourly()
        self._total()
        self._results()

    def _hourly(self):
        # Grup data by hour, select only energies, copy data in new place, add hour grups to get total
        select = ['timestamp', 'energyP', 'energyG', 'energyA']
        on_off = ['on_offL1', 'on_offL2']
        self.df_in[on_off] = self.df_in[on_off].astype(bool)
        data = self.df_in.groupby(pd.Grouper(key='timestamp', freq='H'), as_index=False)
        self.df_hour = data[select].last().copy()
        data_h_sum = data.sum()

        # Energy in system
        self.df_hour.insert(1, 'energySY', self.df_hour['energyP'].values + self.df_hour['energyG'].values)

        # General energyes
        self.df_hour['energyC'] = data_h_sum['powerC'].values*self.Ts/3600
        self.df_hour['energyLB'] = data_h_sum['powerLB'].values*self.Ts/3600
        self.df_hour['energyL1'] = data_h_sum['powerL1'].values*self.Ts/3600
        self.df_hour['energyL2'] = data_h_sum['powerL2'].values*self.Ts/3600

        # Find aprox loads of each one
        self.aprox_loads = {'powerLB':0, 'powerL1':0, 'powerL2':0}
        for k in self.aprox_loads:
            df = self.df_in[k][self.df_in[k] > 0]
            if (suma := df.sum()):
                self.aprox_loads[k] = suma / df.count()

        # Energy Consumed Max
        energy_cm = sum(self.aprox_loads.values())
        tmp = self.df_hour['energyP'].copy()
        tmp[self.df_hour['energyP'] >= energy_cm] = energy_cm
        self.df_hour['energyCM'] = tmp

        # Energy Surplus
        energy_s = self.df_hour['energyP'].values - self.df_hour['energyCM'].values
        energy_s[self.df_hour['energyC'] > energy_cm] = 0
        self.df_hour['energyS'] = energy_s

        # Energy Lost
        energy_l = self.df_hour['energyA'].values - energy_s
        energy_l[energy_l < 0] = 0
        self.df_hour['energyL'] = energy_l

        # Efficiency
        with np.errstate(divide='ignore', invalid='ignore'):
            self.df_hour['efficiency'] = 100 - self.df_hour['energyL'].values/self.df_hour['energyCM'].values
        self.df_hour.loc[self.df_hour['efficiency'].values < 0, 'efficiency'] = 100
        self.df_hour['efficiency'] = self.df_hour['efficiency'].fillna(100)

        # Commutations
        self.df_hour[on_off] = data_h_sum[on_off]

        # Price
        if self.df_price is not None:
            self.df_hour['balance'] = (self.df_hour['energyS'].values*self.sell_price - self.df_hour['energyL'].values*self.df_price.values)/100 # W * €/kWh -> €/1000 | €/1000 * 10 -> cént.

    def _total(self):
        # Energy Balance - Add hourly columns to get one row series of the total        
        self.df_total = self.df_hour.sum(numeric_only=True).rename('energyT')
        self.df_total = self.df_total.to_frame()
        self.df_total.loc['efficiency',:] = self.df_total.loc['efficiency',:] / self.df_hour.iloc[:,0].count()
        self.df_total['energyDT'] = self.df_total['energyT'].mul(self.sim_days)
        self.df_total = self.df_total.T
            
    def _results(self):
        # Commutations
        dic = {
            'loadB': 0,
            'load1': self.df_total['on_offL1'].values[0],
            'load2': self.df_total['on_offL2'].values[0]
        }
        dic['total'] = dic['load1'] + dic['load2']
        commutations = pd.Series(dic)
        daily_com = commutations*self.sim_days

        # Time On/Powered
        select = ['powerLB', 'powerL1', 'powerL2']
        name = ['loadB', 'load1', 'load2']
        samples_on = self.df_in[select][self.df_in[select] > 0].count()
        samples_on.rename(dict(zip(select, name)), inplace = True)
        self.df_results.rename(dict(zip(select, name)), inplace = True)
        hours_on = samples_on*self.Ts/3600
        hours_on_daily = hours_on*self.sim_days

        # Aprox Loads
        for i, key in enumerate(select):
            self.aprox_loads[name[i]] = self.aprox_loads.pop(key)

        # Convert to dataframe
        dic = {
            'loadAprox': self.aprox_loads,
            'efficiency': {'total': self.df_total['efficiency'].values[0]}, 
            'balance': {'total': self.df_total['balance'].values[0]}, 
            'commut':commutations,  'commutD':daily_com, 
            'samplesOn':samples_on,  'hoursOn':hours_on, 'hoursOnD': hours_on_daily
        }
        self.df_results = pd.concat([self.df_results, pd.DataFrame.from_dict(dic)], axis=1)
        self.df_results = self.df_results.reindex(['loadB', 'load1', 'load2', 'total'])

        