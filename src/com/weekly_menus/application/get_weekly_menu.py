import inject, datetime

from .add_weekly_menu import merge_weekly_menu
from ..domain.weekly_menu import get_week_number, WeeklyMenu
from ..domain.weekly_menu_database import WeeklyMenuDatabase
from ..domain.weekly_menu_exception import WeeklyMenuException
from ...menus.application.get_menu import GetMenu
from ...utils.log import Log


class GetWeeklyMenu:
    @inject.autoparams()
    def __init__(self, database: WeeklyMenuDatabase, get_menu: GetMenu, log: Log):
        self.__database = database
        self.__get_menu = get_menu
        self.__log = log

    def execute(self, username, year_week):
        try:
            self.__log.trace('GetWeeklyMenu {0}, {1}', username, year_week)
            date_time = datetime.datetime.strptime(year_week + '-1', "%Y-W%W-%w")
            week_number = get_week_number(date_time)
            weekly_menu = self.__database.find(username, week_number)
            return weekly_menu
        except WeeklyMenuException:
            menus = self.__get_menu.execute({'username': username, 'year_week': year_week})
            weekly_menu = WeeklyMenu(None, date_time.strftime('%Y-%m-%d')).to_json()
            for menu in menus:
                data = {
                    'username': menu['username'],
                    'date': menu['date'],
                    'nutritional_value': menu['nutritional_value'],
                    'menu': menu
                }
                weekly_menu = merge_weekly_menu(weekly_menu, WeeklyMenu(data), self.__log)

            return weekly_menu
