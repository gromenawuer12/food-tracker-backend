import inject, datetime
from ..domain.monthly_menu_database import MonthlyMenuDatabase

class GetMonthlyMenu:
    @inject.autoparams()
    def __init__(self, database: MonthlyMenuDatabase):
        self.__database = database

    def execute(self, user, monthlyNumber):
        if monthlyNumber is None:
            todayMonthlyNumber = datetime.date.today().strftime("%Y-%m")
            response = self.__database.find(user, todayMonthlyNumber)
        else:
            response = self.__database.find(user,monthlyNumber)
        return response