import inject
from ..domain.product_database import ProductDatabase


class GetProduct:
    @inject.autoparams()
    def __init__(self, database: ProductDatabase):
        self.__database = database

    def execute(self, name, last_evaluated_key, items_per_page):
        if name is None:
            response = self.__database.findAll(last_evaluated_key, items_per_page)
        else:
            response = self.__database.find(name)
        return response
