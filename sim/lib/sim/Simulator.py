from email.mime import base
from email.policy import default
from sys import builtin_module_names
import pandas as pd
import datetime as dt
from .Load import Load
from .DataFrames import DataFrameIn
from .AlgorithmsConfig import AlgorithmConfig, AlgorithmsEnum, PredictFinalEnergy

class Simulator:

    def __init__(self, df_in:DataFrameIn, min_sec:int=300):
        self.df_in = df_in
        self.df_out = pd.DataFrame()
        self.Ts = self.calc_Ts()
        self.min_sec = min_sec

    def calc_Ts(self):
        return self.df_in.calc_Ts()

    def simulate(self, start:str, end:str, algorithm:AlgorithmConfig, load1:Load, load2:Load, baseload:float=0):
        # Init
        dfRG = self.df_in.select_daterange(start, end, self.min_sec)
        self.df_out = dfRG.df
        self.simulated_nsamples = dfRG.nsamples
        self.simulated_nsec = dfRG.nsec
        current_hour = None
        off_timestamp_limit = dt.datetime.now()
        sim_data = {'powerC':[], 'powerLB':[], 'powerL1':[], 'powerL2':[], 'energyP':[], 'energyA':[], 'on_offL1':[], 'on_offL2':[]}
        #endregion
        
        for _, row in self.df_out.iterrows(): # [Program] while True:
            #region -> Calc/Get Powers/Energies
            power_lb = baseload if isinstance(baseload, (float, int)) else row['powerLB'] # [Simulation]
            timestamp = row['timestamp']
            power_g = row['powerG']
            power_c = power_lb + load1.get_power() + load2.get_power()

            #region -> If hour has passed reset powers
            if current_hour != timestamp.hour:
                energy_a =  0
                current_hour = timestamp.hour
                next_hour = timestamp.replace(second=0, microsecond=0, minute=0) + dt.timedelta(hours=1)
                energy_p = 0 # [Simulation]
            #endregion

            # Calc Available Energy [Wh]
            energy_a = (power_g - power_c) * self.Ts / 3600 + energy_a
            #endregion

            #region -> Algorithm
            on_offL1 = on_offL2 = 0
            match algorithm.type:
                case AlgorithmsEnum.hysteresis:
                    if load1.power > 0:
                        if energy_a >= algorithm.th_top1: 
                            on_offL1 = load1.turn_on()
                        elif energy_a <= algorithm.th_bottom1:
                            on_offL1 = load1.turn_off()
                    if load2.power > 0:
                        if energy_a >= algorithm.th_top2: 
                            on_offL2 = load2.turn_on()
                        elif energy_a <= algorithm.th_bottom2:
                            on_offL2 = load2.turn_off()
                
                case AlgorithmsEnum.min_on_time:
                    time_to_use = energy_a/load1.power * 3600 # [s] <- Wh/W = h
                    time_limit = algorithm.time_limit
                    if time_to_use >= time_limit:
                        off_timestamp_limit = timestamp + dt.timedelta(seconds=time_limit)
                        on_offL1 = load1.turn_on()
                    elif timestamp >= off_timestamp_limit:
                        on_offL1 = load1.turn_off()

                case AlgorithmsEnum.time_to_consume:
                    time_remaining = (next_hour - timestamp).total_seconds()
                    match algorithm.predict_final_energy:
                        case PredictFinalEnergy.disabled:
                            energy1h = energy_a
                        case PredictFinalEnergy.avarage_power:
                            avg = energy_a / (3600-time_remaining)
                            energy1h = avg*3600
                        case PredictFinalEnergy.project_current_power:
                            energy1h = energy_a + time_remaining*power_g/3600
                    time_to_use = energy1h / load1.power * 3600 # [s] <- Wh/W = h
                    if time_to_use >= time_remaining:
                        on_offL1 = load1.turn_on()
                    elif energy1h <= 0:
                        on_offL1 = load1.turn_off()
            #endregion

            #region -> [Simulation] Calc/Save other energys for data avaluation [Wh]
            energy_p = (power_g * self.Ts) / 3600 + energy_p # Energy Produced
            sim_data['powerC'].append(power_c)
            sim_data['powerLB'].append(power_lb)
            sim_data['powerL1'].append(load1.get_power())
            sim_data['powerL2'].append(load2.get_power())
            sim_data['energyP'].append(energy_p)
            sim_data['energyA'].append(energy_a)
            sim_data['on_offL1'].append(on_offL1)
            sim_data['on_offL2'].append(on_offL2)
            #endregion

        #region -> [Simulation] Store data to pandas dataframe
        for key, value in sim_data.items():
            self.df_out[key] = value
        #endregion

        #region -> [Simulation] Calc the rest of the data
        energy_g = self.df_out['energyA'].copy()
        energy_g[energy_g > 0] = 0
        self.df_out['energyG'] = -energy_g
        self.df_out['energyA'] = self.df_out['energyA'].mask(self.df_out['energyA'] < 0, 0)
        #endregion
        self.simulated = True

    