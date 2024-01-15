import inject

from .add_menu import AddMenu
from ..domain.menu import Menu
from ..domain.menu_database import MenuDatabase
from ..domain.menu_exception import MenuException
from ...utils.log import Log


class EditMenu:
    @inject.autoparams()
    def __init__(self, database: MenuDatabase, add_menu: AddMenu, log: Log):
        self.__database = database
        self.__add_menu = add_menu
        self.log = log

    def execute(self, path_id, menu: Menu):
        attrs = path_id.split('|')
        username = attrs[0]
        date = attrs[1]
        self.log.trace('edit_menu: username={0} & date={1}', username, date)

        menu_old = Menu(self.__database.find(username, date))
        self.log.trace('edit_menu: menu={0}', menu_old.to_json())

        self.__database.delete(username, date)
        self.log.trace('edit_menu: menu with username={0} & date={1} deleted', username, date)
        try:
            self.log.trace('edit_menu: creating menu={0}', menu.to_json())
            self.__add_menu.execute(menu)
        except MenuException as menu_exception:
            self.log.error('edit_menu: error while adding, restoring to {0}', menu_old.to_json())
            self.__database.create(menu_old)
            raise menu_exception
