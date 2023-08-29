from abc import ABC, abstractmethod
from .recipe import Recipe

class RecipeDatabase(ABC):
    @abstractmethod
    def create(self, recipe: Recipe) -> None:
        pass