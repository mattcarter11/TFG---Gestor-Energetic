from enum import Enum

class AlgorithmsEnum(Enum):
    hysteresis = 1
    min_on_time = 2
    time_to_consume = 3

class AlgorithmConfig():
    pass

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

class TimeToConsume(AlgorithmConfig):
       def __init__(self, predict_final_energy:bool):
        self.type = AlgorithmsEnum.time_to_consume
        self.predict_final_energy = predict_final_energy

    