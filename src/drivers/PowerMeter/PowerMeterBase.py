from abc import ABC, abstractmethod

class PowerMeterBase(ABC):

    @abstractmethod
    def power_consumed(self) -> float:
        raise NotImplementedError("Base Class")

    @abstractmethod
    def power_generated(self) -> float:
        raise NotImplementedError("Base Class")

    @abstractmethod
    def power_gc(self) -> tuple:
        raise NotImplementedError("Base Class")

    @abstractmethod
    def power_available(self) -> float:
        raise NotImplementedError("Base Class")