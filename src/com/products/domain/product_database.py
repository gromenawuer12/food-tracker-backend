from abc import ABC, abstractmethod
from .product import Product

class ProductDatabase(ABC):
    @abstractmethod
    def create(self, product: Product) -> None:
        pass

    @abstractmethod
    def find_all(self, query, last_evaluated_key, items_per_page):
        pass