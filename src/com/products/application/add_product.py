import inject
from ..domain.product import Product
from ..domain.product_database import ProductDatabase


class AddProduct:
    @inject.autoparams()
    def __init__(self, database: ProductDatabase):
        self.__database = database

    def execute(self, product: Product):
        self.__database.create(product)