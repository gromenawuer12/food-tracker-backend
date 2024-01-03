import inject
from ..domain.nutritional_value import NutritionalValue
from ..domain.nutritional_value_database import NutritionalValueDatabase
from ..domain.nutritional_value_exception import NutritionalValueException
from ...utils.log import Log


class EditNutritionalValue:
    @inject.autoparams()
    def __init__(self, database: NutritionalValueDatabase, log: Log):
        self.__database = database
        self.log = log

    def execute(self, shortname, nutritional_value):
        nutritional_value_old = NutritionalValue(self.__database.find(shortname))
        self.log.trace('EditNutritionalValue: nutritionalValue={0}', nutritional_value_old.to_json())

        self.__database.delete(shortname)
        self.log.trace('EditNutritionalValue: unit with shortname={0} deleted', shortname)
        try:
            self.log.trace('EditNutritionalValue: creating nutritionalValue={0}', nutritional_value.to_json())
            self.__database.create(nutritional_value)
        except NutritionalValueException as nutritional_value_exception:
            self.log.error('EditNutritionalValue: error while adding, restoring to {0}', nutritional_value_old.to_json())
            self.__database.create(nutritional_value_old)
            raise nutritional_value_exception
