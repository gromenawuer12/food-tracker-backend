import inject
from ..domain.weekly_menu import WeeklyMenu
from ..domain.weekly_menu_database import WeeklyMenuDatabase


class AddWeeklyMenu:
    @inject.autoparams()
    def __init__(self, database: WeeklyMenuDatabase):
        self.__database = database

    def execute(self, weeklyMenu: WeeklyMenu):
        old_data = self.__database.find(weeklyMenu.user, weeklyMenu.weekly_number)

        if old_data:
            for nutritional_value in weeklyMenu.nutritional_value:
                if nutritional_value in old_data['nutritional_value']:
                    old_data['nutritional_value'][nutritional_value] = str(
                        float(old_data['nutritional_value'][nutritional_value]) + float(
                            weeklyMenu.nutritional_value[nutritional_value]))
                else:
                    old_data['nutritional_value'][nutritional_value] = weeklyMenu.nutritional_value[nutritional_value]
            self.__database.updateNutritionalValue(weeklyMenu.user, weeklyMenu.weekly_number,
                                                   old_data['nutritional_value'])
        else:
            self.__database.create(weeklyMenu)
