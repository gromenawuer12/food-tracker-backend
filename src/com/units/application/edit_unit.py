import inject
from ..domain.unit import Unit
from ..domain.unit_database import UnitDatabase
from ..domain.unit_exception import UnitException
from ...utils.log import Log


class EditUnit:
    @inject.autoparams()
    def __init__(self, database: UnitDatabase, log: Log):
        self.__database = database
        self.log = log

    def execute(self, shortname, unit):
        unit_old = Unit(self.__database.find(shortname))
        self.log.trace('edit_unit: unit={0}', unit_old.to_json())

        self.__database.delete(shortname)
        self.log.trace('edit_unit: unit with shortname={0} deleted', shortname)
        try:
            self.log.trace('edit_unit: creating unit={0}', unit.to_json())
            self.__database.create(unit)
        except UnitException as unitException:
            self.log.error('edit_unit: error while adding, restoring to {0}', unit_old.to_json())
            self.__database.create(unit_old)
            raise unitException
