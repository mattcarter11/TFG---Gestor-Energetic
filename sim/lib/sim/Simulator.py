import pandas as pd
import datetime as dt

from sqlalchemy import column
from .Load import Load
from .DataFrames import DataFrameIn
from .AlgorithmsConfig import AlgorithmConfig, AlgorithmsEnum, PredictFinalEnergy

class Simulator:

    def __init__(self, df_in:DataFrameIn, min_sec:int=300):
        df_in.rearange_cols()
        self.df_in = df_in
        self.df_out = None
        self.Ts = df_in.calc_Ts()
        self.min_sec = min_sec

    def simulate(self, start:str, end:str, algorithm:AlgorithmConfig, load1:Load, load2:Load, baseload:float=0):
        #region -> Init
        dfRG = self.df_in.select_daterange(start, end, self.min_sec)
        self.simulated_nsamples = dfRG.nsamples
        self.simulated_nsec = dfRG.nsec
        current_hour = None
        off_timestamp_limit = dt.datetime.now()
        sim_data = {'powerC':[], 'powerLB':[], 'powerL1':[], 'powerL2':[], 'energyP':[], 'energyA':[], 'on_offL1':[], 'on_offL2':[]}
        #endregion
        
        for row in dfRG.df.to_dict('records'):  #x5..10 Faster vs .iterrows()
            #region -> Calc/Get Powers/Energies
            power_lb = baseload if isinstance(baseload, (float, int)) else row['powerLB'] # [Simulation]
            timestamp = row['timestamp']
            power_g = row['powerG']
            power_c = power_lb + load1.get_power() + load2.get_power()
            power_a = power_g - power_c

            #region -> If hour has passed reset powers
            if current_hour != timestamp.hour:
                energy_a = energy_p =  0 # [Simulation] energy_p
                current_hour = timestamp.hour
                next_hour = timestamp.replace(second=0, microsecond=0, minute=0) + dt.timedelta(hours=1)
            #endregion

            # Calc Available Energy [Wh]
            energy_a = (power_a) * self.Ts / 3600 + energy_a
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
                    if time_to_use >= algorithm.min_on_time:
                        off_timestamp_limit = timestamp + dt.timedelta(seconds=algorithm.min_on_time)
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
                            energy1h = energy_a + time_remaining*(power_a)/3600

                    time_to_use = energy1h / load1.power * 3600 # [s] <- Wh/W = h
                    
                    if not load1.on and energy1h >= algorithm.on_min_energy:
                        if time_to_use >= (time_remaining*algorithm.time_factor):
                            on_offL1 = load1.turn_on()
                    elif load1.on:
                        energy1h = energy_a + (power_a + load1.get_power()) * time_remaining
                        if energy1h <= algorithm.end_at_energy:
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
            dfRG.df[key] = value
        #endregion

        dfRG.split_energyA()
        dfRG.rearange_cols()
        self.df_out = dfRG.df
        self.simulated = True

    