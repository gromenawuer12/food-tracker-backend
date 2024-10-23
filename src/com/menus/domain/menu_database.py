from abc import ABC, abstractmethod
from .menu import Menu

class MenuDatabase(ABC):
    @abstractmethod
    def create(self, menu: Menu) -> None:
        pass

    @abstractmethod
    def find(self, username, date):
        pass