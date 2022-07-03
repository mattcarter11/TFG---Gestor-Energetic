from abc import ABC, abstractmethod

class PowerMeterBase(ABC):

    def __init__(self, timeout:int=5, zero_ref:int=20):
        self.timeout = timeout
        self.zero_ref = zero_ref

    @abstractmethod
    def power_consumed(self) -> float:
        raise NotImplementedError("Base Class")

    @abstractmethod
    def power_produced(self) -> float:
        raise NotImplementedError("Base Class")

    @abstractmethod
    def power_pc(self) -> tuple:
        '''returns power produced and consumed in a tuple: (produced, consumed)'''
        raise NotImplementedError("Base Class")

    @abstractmethod
    def power_available(self) -> float:
        raise NotImplementedError("Base Class")