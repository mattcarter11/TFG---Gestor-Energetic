import pandas as pd
import numpy as np
from .DataFrames import DataFrameOut 
from .constants import COL_ORDER

class Results:

    def __init__(self, df:DataFrameOut, df_price=None, sell_price:float|int=0.1):
        df.fill_missing_energy()
        self.Ts = df.Ts
        self.nsec = df.nsec
        self.sim_hours = self.nsec/3600
        self.sim_days = 24/self.sim_hours
        self.sell_price = sell_price
        self.df_price = df_price
        self.df_in = df.df.copy()
        self.df_hour = pd.DataFrame()
        self.df_total = pd.DataFrame()
        self.df_results = pd.DataFrame()
        self.aprox_loads = df.aproximate_loads()
        self.aprox_max_load = df.aproximate_max_load()
        self._hourly()
        self._total()
        self._results()

    def _hourly(self):
        # Grup data by hour, select only energies, copy data in new place, add hour grups to get total
        select = ['timestamp', 'energyP', 'energyB', 'energyGD', 'energyAB']
        on_off = ['on_offL1', 'on_offL2']
        self.df_in[on_off] = self.df_in[on_off].astype(bool)
        data = self.df_in.groupby(pd.Grouper(key='timestamp', freq='H'), as_index=False)
        self.df_hour = data[select].last().copy()
        data_h_sum = data.sum()

        # General energyes
        self.df_hour['energyG'] = data_h_sum['powerG'].values*self.Ts/3600
        self.df_hour['energyGP'] = data_h_sum['powerGP'].values*self.Ts/3600
        self.df_hour['energyC'] = data_h_sum['powerC'].values*self.Ts/3600
        self.df_hour['energyLB'] = data_h_sum['powerLB'].values*self.Ts/3600
        self.df_hour['energyL1'] = data_h_sum['powerL1'].values*self.Ts/3600
        self.df_hour['energyL2'] = data_h_sum['powerL2'].values*self.Ts/3600
        self.df_hour['energySY'] = self.df_hour['energyP'].values + self.df_hour['energyG'].values
        self.df_hour['energyGR'] = self.df_hour['energyG'].values - self.df_hour['energyGD'].values
        self.df_hour['energyGnP'] = self.df_hour['energyG'].values - self.df_hour['energyGP'].values
        self.df_hour['energyPC'] = self.df_hour['energyC'].values - self.df_hour['energyG'].values
        self.df_hour['energyPL'] = self.df_hour['energyP'].values - self.df_hour['energyPC'].values
        self.df_hour.loc[np.abs(self.df_hour['energyGR']) < 0.00001, 'energyGR'] = 0
       
        # Energy Consumed Max
        tmp = self.df_hour['energyP'].copy()
        tmp[self.df_hour['energyP'] >= self.aprox_max_load] = self.aprox_max_load
        self.df_hour['energyCM'] = tmp

        # Energy Surplus
        energy_s = self.df_hour['energyP'].values - self.df_hour['energyCM'].values
        self.df_hour['energyS'] = energy_s

        # Energy Lost
        energy_l = self.df_hour['energyAB'].values - energy_s
        energy_l[energy_l < 0] = 0
        self.df_hour['energyL'] = energy_l

        # Price
        if self.df_price is not None:
            buy_price = [self.df_price.values[hour-1] for hour in self.df_hour['timestamp'].dt.hour]
            self.df_hour['balance'] = (self.df_hour['energyAB'].values*self.sell_price - self.df_hour['energyGD'].values*buy_price)/100 # W * €/kWh -> €/1000 | €/1000 * 10 -> cént.

        # Efficiency Con. Max
        with np.errstate(divide='ignore', invalid='ignore'):
            self.df_hour['efficC'] = 100 - (self.df_hour['energyL'].values/self.df_hour['energyCM'].values)*100
            self.df_hour['efficGR'] = (self.df_hour['energyGR'].values/self.df_hour['energyGP'].values)*100

        # Commutations
        self.df_hour[on_off] = data_h_sum[on_off]

        columns = [col for col in COL_ORDER if col in self.df_hour.columns]
        self.df_hour = self.df_hour[[columns[0]]+columns[3:]+columns[1:3]]

    def _total(self):
        # Energy Balance - Add hourly columns to get one row series of the total        
        self.df_total = self.df_hour.sum(numeric_only=True).rename('energyT')
        self.df_total = self.df_total.to_frame()
        with np.errstate(divide='ignore', invalid='ignore'):
            self.df_total.loc['efficC',:] = 100 - (self.df_total.loc['energyL',:]/self.df_total.loc['energyCM',:])*100
            self.df_total.loc['efficGR',:] = (self.df_total.loc['energyGR',:]/self.df_total.loc['energyGP',:])*100
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
        total = 0
        for i, key in enumerate(select):
            val = self.aprox_loads.pop(key)
            self.aprox_loads[name[i]] = val
            total += val
        self.aprox_loads['total'] = total

        # Convert to dataframe
        dic = {
            'loadApprox': self.aprox_loads,
            'efficC': {'total': self.df_total['efficC'].values[0]}, 
            'efficGR': {'total': self.df_total['efficGR'].values[0]}, 
            'balance': {'total': self.df_total['balance'].values[0]}, 
            'commut':commutations,  'commutD':daily_com, 
            'samplesOn':samples_on,  'hoursOn':hours_on, 'hoursOnD': hours_on_daily
        }
        self.df_results = pd.concat([self.df_results, pd.DataFrame.from_dict(dic)], axis=1)
        self.df_results = self.df_results.reindex(['loadB', 'load1', 'load2', 'total'])

        