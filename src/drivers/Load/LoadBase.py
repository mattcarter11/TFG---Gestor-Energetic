from abc import ABC, abstractmethod

class LoadBase(ABC):

    def __init__(self, value:int=0, on_time:int=None):
        self.value = value
        self.on_time = on_time

    @abstractmethod
    def set_status(self, status:bool, timer:int=None):
        raise NotImplementedError("Base Class")

    @abstractmethod
    def get_status(self) -> dict:
        '''Returns the folowing dict: { "ison": bool, "power": float }'''
        raise NotImplementedError("Base Class")

    @abstractmethod
    def get_power(self) -> float:
        raise NotImplementedError("Base Class")