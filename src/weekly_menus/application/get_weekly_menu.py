import inject, datetime
from ..domain.weekly_menu_database import WeeklyMenuDatabase

class GetWeeklyMenu:
    @inject.autoparams()
    def __init__(self, database: WeeklyMenuDatabase):
        self.__database = database

    def execute(self, user, weeklyNumber):
        if weeklyNumber is None:
            today = datetime.date.today()
            auxTuple = datetime.date(today.year,today.month,today.day).isocalendar()
            todayWeeklyNumber = str(auxTuple[0])+"-"+str(auxTuple[1])
            response = self.__database.find(user, todayWeeklyNumber)
        else:
            response = self.__database.find(user, weeklyNumber)
        return response