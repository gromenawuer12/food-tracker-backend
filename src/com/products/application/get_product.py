import inject
from ..domain.product_database import ProductDatabase


class GetProduct:
    @inject.autoparams()
    def __init__(self, database: ProductDatabase):
        self.__database = database

    def execute(self, name):
        if name is None:
            response = self.__database.findAll()
        else:
            response = self.__database.find(name)
        return response
