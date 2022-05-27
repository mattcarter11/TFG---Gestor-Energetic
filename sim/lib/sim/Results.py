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
        self.df_hour.insert(1, 'energySY', (self.df_hour['energyP'] + self.df_hour['energyG']).values)

        # General energyes
        self.df_hour['energyC'] = (data_h_sum['powerC']*self.dfI.Ts/3600).values
        self.df_hour['energyLB'] = (data_h_sum['powerLB']*self.dfI.Ts/3600).values
        self.df_hour['energyL1'] = (data_h_sum['powerL1']*self.dfI.Ts/3600).values
        self.df_hour['energyL2'] = (data_h_sum['powerL2']*self.dfI.Ts/3600).values

        # Energy Consumed Max
        dic = {'powerLB':0, 'powerL1':0, 'powerL2':0}
        for k in dic:
            df = self.dfI.df[k][self.dfI.df[k] > 0]
            if (suma := df.sum()):
                dic[k] = suma / df.count()
        energy_cm = sum(dic.values())
        self.df_hour['energyCM'] = energy_cm
        self.df_load_aprox = pd.DataFrame.from_dict(dic, orient='index')
        self.df_load_aprox.rename(columns={ self.df_load_aprox.columns[0]: "Aprox. Power [W]" }, inplace = True)

        # Energy Surplus
        energy_s = (self.df_hour['energyP'] - energy_cm).values
        energy_s[energy_s < 0] = 0
        energy_s[self.df_hour['energyC'] > energy_cm] = 0
        self.df_hour['energyS'] = energy_s

        # Energy Lost
        energy_l = (self.df_hour['energyA'] - energy_s).values
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

        # Commutations
        dic = {'Base Load': 0}
        dic['Load 1'] = self.dfI.df['on_offL1'].astype(bool).sum(axis=0)
        dic['Load 2'] = self.dfI.df['on_offL2'].astype(bool).sum(axis=0)
        commutations = pd.Series(dic)
        dayly_com = commutations*sim_days

        # Time On/Powered
        select = ['powerLB', 'powerL1', 'powerL2']
        name = ['Base Load', 'Load 1', 'Load 2']
        samples_on = self.dfI.df[select][self.dfI.df[select] > 0].count()
        samples_on.rename(dict(zip(select, name)), inplace = True)
        hours_on = samples_on*self.dfI.Ts/3600
        hours_on_daily = hours_on*sim_days

        # Convert to dataframe
        dic = {'Commutations':commutations, 'Daily Commutations':dayly_com, 'Time On [samples]':samples_on, 'Time On [h]':hours_on, 'Daily Time On [h/day]': hours_on_daily}
        self.df_results = pd.DataFrame.from_dict(dic).T

        