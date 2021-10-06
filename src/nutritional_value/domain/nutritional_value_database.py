from abc import ABC, abstractmethod
from .nutritional_value import NutritionalValue

class NutritionalValueDatabase(ABC):
    @abstractmethod
    def create(self, nutritionalValue: NutritionalValue) -> None:
        pass