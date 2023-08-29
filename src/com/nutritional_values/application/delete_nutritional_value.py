import inject
from ..domain.nutritional_value import NutritionalValue
from ..domain.nutritional_value_database import NutritionalValueDatabase

class DeleteNutritionalValue:
    @inject.autoparams()
    def __init__(self, database: NutritionalValueDatabase):
        self.__database = database

    def execute(self, shortname) -> str:
        self.__database.delete(shortname)
        return "Deleted"