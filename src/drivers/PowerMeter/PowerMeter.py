from abc import ABC, abstractmethod

class PowerMeter(ABC):

    @abstractmethod
    def power_consumed(self) -> float: pass

    @abstractmethod
    def power_generated(self) -> float: pass

    @abstractmethod
    def power_gc(self) -> float: pass