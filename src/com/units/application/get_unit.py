import inject
from ..domain.unit_database import UnitDatabase
from ...utils.log import Log


class GetUnit:
    @inject.autoparams()
    def __init__(self, log: Log, database: UnitDatabase):
        self.__database = database
        self.__log = log

    def execute(self, shortname):
        if shortname is None:
            response = self.__database.find_all()
        else:
            response = self.__database.find(shortname)
        return response
