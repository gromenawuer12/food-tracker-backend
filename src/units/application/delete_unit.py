import inject
from ..domain.unit import Unit
from ..domain.unit_database import UnitDatabase

class DeleteUnit:
    @inject.autoparams()
    def __init__(self, database: UnitDatabase):
        self.__database = database

    def execute(self, shortname) -> str:
        self.__database.delete(shortname)
        return "Deleted"