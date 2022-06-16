from abc import ABC, abstractmethod

class LoadBase(ABC):

    def __init__(self, value:int=0, on_time:int=None):
        self.value = value
        self.on_time = on_time
        self.__load = None

    @abstractmethod
    def set_status(self, status:bool, timer:int=None):
        raise NotImplementedError("Base Class")

    @abstractmethod
    def get_status(self) -> bool:
        raise NotImplementedError("Base Class")

    @abstractmethod
    def get_power(self) -> float:
        raise NotImplementedError("Base Class")