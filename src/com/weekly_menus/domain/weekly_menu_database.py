from abc import ABC, abstractmethod
from .weekly_menu import WeeklyMenu

class WeeklyMenuDatabase(ABC):
    @abstractmethod
    def create(self, weeklyMenu: WeeklyMenu) -> None:
        pass

    @abstractmethod
    def find(self, username, week_number):
        pass