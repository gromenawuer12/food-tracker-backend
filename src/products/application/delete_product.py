import inject
from ..domain.product import Product
from ..domain.product_database import ProductDatabase

class DeleteProduct:
    @inject.autoparams()
    def __init__(self, database: ProductDatabase):
        self.__database = database

    def execute(self, name) -> str:
        self.__database.delete(name)
        return "Deleted"