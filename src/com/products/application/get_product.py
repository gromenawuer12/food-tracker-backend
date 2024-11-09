import inject
from ..domain.product_database import ProductDatabase


class GetProduct:
    @inject.autoparams()
    def __init__(self, database: ProductDatabase):
        self.__database = database

    def execute(self, name, query=None, last_evaluated_key=None, items_per_page=None):
        if name is None:
            response = self.__database.find_all(query, last_evaluated_key, items_per_page)
        else:
            response = self.__database.find(name)
        return response
