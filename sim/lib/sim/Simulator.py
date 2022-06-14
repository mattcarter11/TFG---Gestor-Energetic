import datetime as dt
from .Load import Load
from .DataFrames import DataFrameIn, DataFrameOut
from .AlgorithmsConfig import AlgorithmConfig, AlgorithmsEnum, PredictFinalEnergy

def simulate(df_in:DataFrameIn, algorithm:AlgorithmConfig, load1:Load, load2:Load, baseload:float|int|None=0):
    #region -> Init
    use_df_bl = isinstance(df_in, DataFrameOut) and baseload is None
    current_hour = None
    off_timestamp_limit = dt.datetime.now()
    sim_data = {'powerC':[], 'powerLB':[], 'powerL1':[], 'powerL2':[], 'energyP':[], 'energyA':[], 'on_offL1':[], 'on_offL2':[]}
    #endregion

    for row in df_in.df.to_dict('records'):  #x5..10 Faster vs .iterrows() | x2 faster if df only has necesary columns
        #region -> Calc/Get Powers/Energies
        power_lb = row['powerLB'] if use_df_bl else baseload # [Simulation]
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
        energy_a = (power_a) * df_in.Ts / 3600 + energy_a
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

                on_offL1 = _TTC_load_control(load1, energy_a, power_a, energy1h, time_remaining, algorithm)

                energy1h = energy1h - load1.get_power() * time_remaining / 3600
                power_a = power_a + load1.get_power()
                on_offL2 = _TTC_load_control(load2, energy_a, power_a, energy1h, time_remaining, algorithm)


        #endregion

        #region -> [Simulation] Calc/Save other energys for data avaluation [Wh]
        energy_p = (power_g * df_in.Ts) / 3600 + energy_p # Energy Produced
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
    df_out = df_in.df.copy()
    for key, value in sim_data.items():
        df_out[key] = value
    #endregion

    df_out = DataFrameOut(df_out, False)
    df_out.split_energyA()
    df_out.rearange_cols()
    return df_out
    
def _TTC_load_control(load:Load, energy_a:float, power_a:float, energy1h:float, time_remaining:float, algorithm:AlgorithmConfig):
    if load.power > 0:
        if not load.on:
            if energy1h >= algorithm.on_min_energy:
                time_to_use = energy1h / load.power * 3600 # [s] <- Wh/W = h
                if time_to_use >= (time_remaining*algorithm.time_factor):
                    return load.turn_on()
        else:
            energy1h_if_off = energy_a + (power_a + load.get_power()) * time_remaining / 3600
            if energy1h_if_off <= algorithm.end_at_energy:
                return load.turn_off()
    return 0