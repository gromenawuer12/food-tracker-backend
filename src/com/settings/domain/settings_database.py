from abc import ABC, abstractmethod

from .settings import Settings


class SettingsDatabase(ABC):
    @abstractmethod
    def create(self, settings: Settings) -> None:
        pass

    @abstractmethod
    def delete(self, shortname: str) -> None:
        pass

    @abstractmethod
    def find(self, shortname: str) -> str:
        pass
