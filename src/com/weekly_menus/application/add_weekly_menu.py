import inject
from ..domain.weekly_menu import WeeklyMenu
from ..domain.weekly_menu_database import WeeklyMenuDatabase
from ..domain.weekly_menu_exception import WeeklyMenuException
from ...nutritional_values.domain.nutritional_value import str_sum
from ...utils.log import Log


def merge_weekly_menu(old_weekly_menu, new_weekly_menu, log: Log):
    log.trace('merge_weekly_menu {0} ------ {1}', old_weekly_menu, new_weekly_menu.to_json())
    old_weekly_menu['menus'][new_weekly_menu.menu['date']] = new_weekly_menu.menu
    for nutritional_value in new_weekly_menu.nutritional_value:
        log.trace('AddWeeklyMenu has nutritional_value={0}?', nutritional_value)
        if nutritional_value in old_weekly_menu['nutritional_value']:
            log.trace('AddWeeklyMenu yes it has {0}', old_weekly_menu['nutritional_value'][nutritional_value])
            old_weekly_menu['nutritional_value'][nutritional_value]['value'] = str_sum(
                old_weekly_menu['nutritional_value'][nutritional_value]['value'],
                new_weekly_menu.nutritional_value[nutritional_value]['value']
            )
        else:
            old_weekly_menu['nutritional_value'][nutritional_value] = {
                'name': new_weekly_menu.nutritional_value[nutritional_value]['name'],
                'value': new_weekly_menu.nutritional_value[nutritional_value]['value'],
                'unit': new_weekly_menu.nutritional_value[nutritional_value]['unit']
            }
    return old_weekly_menu


class AddWeeklyMenu:
    @inject.autoparams()
    def __init__(self, database: WeeklyMenuDatabase, log: Log):
        self.__database = database
        self.__log = log

    def execute(self, weekly_menu: WeeklyMenu):
        self.__log.debug('AddWeeklyMenu weeklyMenu={0}', weekly_menu.to_json())
        old_data = None
        try:
            old_data = self.__database.find(weekly_menu.username, weekly_menu.weekly_number)
        except WeeklyMenuException:
            self.__log.debug('AddWeeklyMenu This week not have menus weeklyMenu={0}', weekly_menu)

        if old_data:
            self.__log.debug('AddWeeklyMenu Updating weeklyMenu={0}', old_data)
            self.__log.trace('AddWeeklyMenu adding menu={0}', weekly_menu.menus)
            old_data = merge_weekly_menu(old_data, weekly_menu, self.__log)
            self.__database.update_nutritional_value(weekly_menu.username, weekly_menu.weekly_number,
                                                     old_data['nutritional_value'], old_data['menus'])
        else:
            self.__database.create(weekly_menu)
