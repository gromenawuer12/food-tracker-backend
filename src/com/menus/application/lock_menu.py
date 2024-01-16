import inject
from ..domain.menu_database import MenuDatabase
from ...monthly_menus.domain.monthly_menu import MonthlyMenu
from ...utils.log import Log
from ...weekly_menus.application.add_weekly_menu import AddWeeklyMenu
from ...weekly_menus.domain.weekly_menu import WeeklyMenu
from ...monthly_menus.application.add_monthly_menu import AddMonthlyMenu


class LockMenu:
    @inject.autoparams()
    def __init__(self, database: MenuDatabase, add_weekly_menu: AddWeeklyMenu, add_monthly_menu: AddMonthlyMenu,
                 log: Log):
        self.__database = database
        self.__add_weekly_menu = add_weekly_menu
        self.__add_monthly_menu = add_monthly_menu
        self.__log = log

    def execute(self, date):
        self.__log.trace('LockMenu')
        menus = self.__database.find_lt_date(date)

        if menus:
            for menu in menus:
                self.__log.trace('LockMenu locking menu={0}', menu)
                data = {
                    'username': menu['username'],
                    'date': menu['date'],
                    'nutritional_value': menu['nutritional_value'],
                    'menu': menu
                }
                self.__add_weekly_menu.execute(
                    WeeklyMenu(data)
                )
                self.__database.delete(menu['username'], menu['date'])
