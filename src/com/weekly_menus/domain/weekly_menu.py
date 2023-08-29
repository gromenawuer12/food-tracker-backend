import datetime


class WeeklyMenu():
    def __init__(self, params):
        self.user = params['user']
        self.weekly_number = params['date']
        self.nutritional_value = params['nutritional_value']

    @property
    def weekly_number(self):
        return self._weekly_number

    @weekly_number.setter
    def weekly_number(self, weekly_number):
        aux_date = datetime.datetime.strptime(weekly_number, "%Y-%m-%d")
        aux_tuple = datetime.date(aux_date.year, aux_date.month, aux_date.day).isocalendar()
        self._weekly_number = str(aux_tuple[0]) + "-" + str(aux_tuple[1])
