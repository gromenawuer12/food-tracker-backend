import inject, datetime
from ..domain.monthly_menu_database import MonthlyMenuDatabase


class GetMonthlyMenu:
    @inject.autoparams()
    def __init__(self, database: MonthlyMenuDatabase):
        self.__database = database

    def execute(self, user, monthly_number):
        if monthly_number is None:
            today_monthly_number = datetime.date.today().strftime("%Y-%m")
            response = self.__database.find(user, today_monthly_number)
        else:
            response = self.__database.find(user, monthly_number)
        return response
