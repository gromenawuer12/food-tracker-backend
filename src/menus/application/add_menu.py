import inject
from ..domain.menu import Menu
from ..domain.menu_database import MenuDatabase

class AddMenu:
    @inject.autoparams()
    def __init__(self, database: MenuDatabase):
        self.__database = database

    def execute(self, menu: Menu) -> str:
        self.__database.create(menu)
        return "Added"