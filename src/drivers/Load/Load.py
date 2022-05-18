from abc import ABC, abstractmethod

class Load(ABC):

    @abstractmethod
    def set_status(self, value:bool, timer:int=None): pass

    @abstractmethod
    def get_status(self) -> bool: pass

    @abstractmethod
    def get_power(self) -> float: pass