import inject
from ..domain.nutritional_value import NutritionalValue
from ..domain.nutritional_value_database import NutritionalValueDatabase

class GetNutritionalValue:
    @inject.autoparams()
    def __init__(self, database: NutritionalValueDatabase):
        self.__database = database

    def execute(self, shortname):
        if shortname is None:
            response = self.__database.findAll()
        else:
            response = self.__database.find(shortname)
        return response