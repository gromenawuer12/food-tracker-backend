import inject
from ..domain.menu_database import MenuDatabase


class GetMenu:
    @inject.autoparams()
    def __init__(self, database: MenuDatabase):
        self.__database = database

    def execute(self, params=None):
        if params is None:
            params = {}

        return self.__database.find_all()
