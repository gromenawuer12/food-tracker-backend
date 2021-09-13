from abc import ABC, abstractmethod
from .user import User

class UserDatabase(ABC):
    @abstractmethod
    def create(self, user: User) -> None:
        pass