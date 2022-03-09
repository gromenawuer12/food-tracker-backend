import inject
from ..domain.monthly_menu import MonthlyMenu
from ..domain.monthly_menu_database import MonthlyMenuDatabase

class AddMonthlyMenu:
    @inject.autoparams()
    def __init__(self, database: MonthlyMenuDatabase):
        self.__database = database

    def execute(self, monthlyMenu: MonthlyMenu) -> str:
        try:
            old_data = self.__database.find(monthlyMenu.user, monthlyMenu.monthly_number)
        except:
            old_data = []

        if old_data:
            for nutritional_value in monthlyMenu.nutritional_value:
                if nutritional_value in old_data['nutritional_value']:
                    old_data['nutritional_value'][nutritional_value]=str(int(old_data['nutritional_value'][nutritional_value])+int(monthlyMenu.nutritional_value[nutritional_value]))
                else:
                    old_data['nutritional_value'][nutritional_value]=monthlyMenu.nutritional_value[nutritional_value]
            self.__database.updateNutritionalValue(monthlyMenu.user, monthlyMenu.monthly_number, old_data['nutritional_value'])
        else:
            self.__database.create(monthlyMenu)

        return "Added"