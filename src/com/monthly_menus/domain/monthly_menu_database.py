from abc import ABC, abstractmethod
from .monthly_menu import MonthlyMenu

class MonthlyMenuDatabase(ABC):
    @abstractmethod
    def create(self, monthlyMenu: MonthlyMenu) -> None:
        pass