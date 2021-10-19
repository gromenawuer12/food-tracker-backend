from abc import ABC, abstractmethod
from .product import Product

class ProductDatabase(ABC):
    @abstractmethod
    def create(self, product: Product) -> None:
        pass