from abc import ABC, abstractmethod
from .unit import Unit

class UnitDatabase(ABC):
    @abstractmethod
    def create(self, unit: Unit) -> None:
        pass