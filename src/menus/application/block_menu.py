import inject
from ..domain.menu_database import MenuDatabase

class BlockMenu:
    @inject.autoparams()
    def __init__(self, database: MenuDatabase):
        self.__database = database

    def execute(self, user, date):
        response = self.__database.findUnlocked(user,date)
        for item in response:
            self.__database.updateIsLocked(user,item["date"])
        return response