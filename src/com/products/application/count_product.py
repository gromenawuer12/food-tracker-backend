import inject
from ..domain.product_database import ProductDatabase


class CountProduct:
    @inject.autoparams()
    def __init__(self, database: ProductDatabase):
        self.__database = database

    def execute(self):
        return self.__database.count()
