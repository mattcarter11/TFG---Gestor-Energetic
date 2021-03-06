from enum import Enum

# Enums represent a multiple choice setting
class AlgorithmType(Enum):
    none = 0
    hysteresis = 1
    min_on_time = 2
    time_to_consume = 3

class PredictFinalEnergy(Enum):
    disabled = 0
    avarage_power = 1
    project_current_power = 2

class MinOnTimeMode(Enum):
    on2_if_on1 = 0
    order = 1
    fastest = 2


# Base class to represent any algorithm
class AlgorithmConfig():
    def __init__(self):
        self.type = AlgorithmType.none


# Each class represents it's agrithm config
class HysteresisConfig(AlgorithmConfig):
    def __init__(self, th_top1:float, th_bottom1:float, th_top2:float, th_bottom2:float):
        self.type       = AlgorithmType.hysteresis
        self.th_top1    = th_top1
        self.th_bottom1 = th_bottom1
        self.th_top2    = th_top2
        self.th_bottom2 = th_bottom2

class MinOnTimeConfig(AlgorithmConfig):
    def __init__(self, time_limit:float, mode:MinOnTimeMode):
        self.type = AlgorithmType.min_on_time
        self.time_limit = time_limit
        self.mode = mode

class TimeToConsume(AlgorithmConfig):
       def __init__(self, predict_final_energy:PredictFinalEnergy, end_at_energy:float, on_min_energy:float, fime_factor:float):
        self.type = AlgorithmType.time_to_consume
        self.predict_final_energy = predict_final_energy
        self.end_at_energy = end_at_energy
        self.on_min_energy = on_min_energy
        self.time_factor = min(1, max(0.01, fime_factor))

    