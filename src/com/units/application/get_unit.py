import inject
from ..domain.unit_database import UnitDatabase


class GetUnit:
    @inject.autoparams()
    def __init__(self, database: UnitDatabase):
        self.__database = database

    def execute(self, shortname):
        if shortname is None:
            response = self.__database.find_all()
        else:
            response = self.__database.find(shortname)
        return response
