import inject
from ..domain.menu_database import MenuDatabase


class DeleteMenu:
    @inject.autoparams()
    def __init__(self, database: MenuDatabase):
        self.__database = database

    def execute(self, user, date) -> str:
        self.__database.delete(user, date)
