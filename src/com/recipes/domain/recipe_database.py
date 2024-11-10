from abc import ABC, abstractmethod
from .recipe import Recipe

class RecipeDatabase(ABC):
    @abstractmethod
    def create(self, recipe: Recipe) -> None:
        pass

    @abstractmethod
    def find_all(self, query, last_evaluated_key, items_per_page) -> None:
        pass