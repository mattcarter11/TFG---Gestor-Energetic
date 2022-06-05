import pandas as pd 
from .DataFrames import DataFrameOut 

class Results:

    def __init__(self, df:DataFrameOut):
        df.fill_missing_power()
        self.dfI = df
        self.df_hour = pd.DataFrame()
        self.df_total = pd.DataFrame()
        self.df_results = pd.DataFrame()
        self._hourly()
        self._total()

    def _hourly(self):
        # Grup data by hour, select only energies, copy data in new place, add hour grups to get total
        data = self.dfI.df.groupby(pd.Grouper(key='timestamp', freq='H'), as_index=False)
        select = ['timestamp', 'energyP', 'energyG', 'energyA']
        self.df_hour = data[select].last().copy()
        data_h_sum = data.sum()

        # Energy in system
        self.df_hour.insert(1, 'energySY', self.df_hour['energyP'].values + self.df_hour['energyG'].values)

        # General energyes
        self.df_hour['energyC'] = data_h_sum['powerC'].values*self.dfI.Ts/3600
        self.df_hour['energyLB'] = data_h_sum['powerLB'].values*self.dfI.Ts/3600
        self.df_hour['energyL1'] = data_h_sum['powerL1'].values*self.dfI.Ts/3600
        self.df_hour['energyL2'] = data_h_sum['powerL2'].values*self.dfI.Ts/3600

        # Energy Consumed Max
        dic = {'powerLB':0, 'powerL1':0, 'powerL2':0}
        for k in dic:
            df = self.dfI.df[k][self.dfI.df[k] > 0]
            if (suma := df.sum()):
                dic[k] = suma / df.count()
        energy_cm = sum(dic.values())
        tmp = self.df_hour['energyP'].copy()
        tmp[self.df_hour['energyP'] >= energy_cm] = energy_cm
        self.df_hour['energyCM'] = tmp
        self.df_results = pd.DataFrame.from_dict(dic, orient='index')
        self.df_results.rename(columns={ self.df_results.columns[0]: "Aprox. Value [W]" }, inplace = True)

        # Energy Surplus
        energy_s = self.df_hour['energyP'].values - self.df_hour['energyCM'].values
        energy_s[self.df_hour['energyC'] > energy_cm] = 0
        self.df_hour['energyS'] = energy_s

        # Energy Lost
        energy_l = self.df_hour['energyA'].values - energy_s
        energy_l[energy_l < 0] = 0
        self.df_hour['energyL'] = energy_l

    def _total(self):
        sim_hours = self.dfI.nsec/3600
        sim_days = 24/sim_hours

        # Energy Balance - Add hourly columns to get one row series of the total        
        self.df_total = self.df_hour.sum(numeric_only=True).rename('Total [Wh]')
        self.df_total = self.df_total.to_frame()
        self.df_total['Daily Total [Wh/day]'] = self.df_total['Total [Wh]'].mul(sim_days)
        self.df_total = self.df_total.T

        # Efficiency
        efficiency = 1 - self.df_total['energyL'].values[0]/self.df_total['energyCM'].values[0]
        efficiency = {'Total':efficiency*100}

        # Commutations
        dic = {'Base Load': None}
        dic['Load 1'] = self.dfI.df['on_offL1'].astype(bool).sum(axis=0)
        dic['Load 2'] = self.dfI.df['on_offL2'].astype(bool).sum(axis=0)
        dic['Total'] = dic['Load 1'] + dic['Load 2']
        commutations = pd.Series(dic)
        daily_com = commutations*sim_days

        # Time On/Powered
        select = ['powerLB', 'powerL1', 'powerL2']
        name = ['Base Load', 'Load 1', 'Load 2']
        samples_on = self.dfI.df[select][self.dfI.df[select] > 0].count()
        samples_on.rename(dict(zip(select, name)), inplace = True)
        self.df_results.rename(dict(zip(select, name)), inplace = True)
        hours_on = samples_on*self.dfI.Ts/3600
        hours_on_daily = hours_on*sim_days

        # Convert to dataframe
        dic = {'Efficiency':efficiency, 'Commutations':commutations, 'Daily Commutations':daily_com, 'Samples On':samples_on, 'Hours On':hours_on, 'Daily Hours On': hours_on_daily}
        self.df_results = pd.concat([self.df_results, pd.DataFrame.from_dict(dic)], axis=1)

        