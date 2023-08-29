import inject, datetime
from ..domain.weekly_menu_database import WeeklyMenuDatabase


class GetWeeklyMenu:
    @inject.autoparams()
    def __init__(self, database: WeeklyMenuDatabase):
        self.__database = database

    def execute(self, user, weekly_number):
        if weekly_number is None:
            today = datetime.date.today()
            aux_tuple = datetime.date(today.year, today.month, today.day).isocalendar()
            today_weekly_number = str(aux_tuple[0]) + "-" + str(aux_tuple[1])
            response = self.__database.find(user, today_weekly_number)
        else:
            response = self.__database.find(user, weekly_number)
        return response
