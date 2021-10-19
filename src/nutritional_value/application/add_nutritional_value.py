import inject
from ..domain.nutritional_value import NutritionalValue
from ..domain.nutritional_value_database import NutritionalValueDatabase

class AddNutritionalValue:
    @inject.autoparams()
    def __init__(self, database: NutritionalValueDatabase):
        self.__database = database

    def execute(self, nutritionalValue: NutritionalValue) -> str:
        self.__database.create(nutritionalValue)
        return "Added"