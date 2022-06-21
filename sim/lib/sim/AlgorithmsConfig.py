from enum import Enum

class AlgorithmsEnum(Enum):
    none = 0
    hysteresis = 1
    min_on_time = 2
    time_to_consume = 3

class AlgorithmConfig():
    def __init__(self):
        self.type = AlgorithmsEnum.none


class HysteresisConfig(AlgorithmConfig):
    def __init__(self, th_top1:float, th_bottom1:float, th_top2:float, th_bottom2:float):
        self.type       = AlgorithmsEnum.hysteresis
        self.th_top1    = th_top1
        self.th_bottom1 = th_bottom1
        self.th_top2    = th_top2
        self.th_bottom2 = th_bottom2

class MinOnTimeConfig(AlgorithmConfig):
    def __init__(self, min_on_time:float):
        self.type = AlgorithmsEnum.min_on_time
        self.min_on_time = min_on_time

class PredictFinalEnergy(Enum):
    disabled = 0
    avarage_power = 1
    project_current_power = 2

class TimeToConsume(AlgorithmConfig):
       def __init__(self, predict_final_energy:PredictFinalEnergy, end_at_energy:float, on_min_energy:float, fime_factor:float):
        self.type = AlgorithmsEnum.time_to_consume
        self.predict_final_energy = predict_final_energy
        self.end_at_energy = end_at_energy
        self.on_min_energy = on_min_energy
        self.time_factor = min(1, max(0.01, fime_factor))

    