import inject
from ..domain.weekly_menu import WeeklyMenu
from ..domain.weekly_menu_database import WeeklyMenuDatabase
from ..domain.weekly_menu_exception import WeeklyMenuException
from ...utils.log import Log


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
            old_data['menus'].append(weekly_menu.menus[0])
            for nutritional_value in weekly_menu.nutritional_value:
                self.__log.trace('AddWeeklyMenu has nutritional_value={0}?', nutritional_value)
                if nutritional_value in old_data['nutritional_value']:
                    self.__log.trace('AddWeeklyMenu yes it has {0}', old_data['nutritional_value'][nutritional_value])
                    old_data['nutritional_value'][nutritional_value]['value'] = str(round(
                        float(old_data['nutritional_value'][nutritional_value]['value']) +
                        float(weekly_menu.nutritional_value[nutritional_value]['value'])
                        , 2)
                    )
                else:
                    old_data['nutritional_value'][nutritional_value] = weekly_menu.nutritional_value[nutritional_value]
            self.__database.update_nutritional_value(weekly_menu.username, weekly_menu.weekly_number,
                                                     old_data['nutritional_value'], old_data['menus'])
        else:
            self.__database.create(weekly_menu)
