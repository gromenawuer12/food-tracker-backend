import inject
from ..domain.unit import Unit
from ..domain.unit_database import UnitDatabase


class AddUnit:
    @inject.autoparams()
    def __init__(self, database: UnitDatabase):
        self.__database = database

    def execute(self, unit: Unit):
        self.__database.create(unit)
