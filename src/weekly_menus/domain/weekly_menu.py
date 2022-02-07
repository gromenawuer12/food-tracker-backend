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
        auxDate = datetime.datetime.strptime(weekly_number,"%Y-%m-%d")
        auxTuple = datetime.date(auxDate.year,auxDate.month,auxDate.day).isocalendar()
        self._weekly_number = str(auxTuple[0])+"-"+str(auxTuple[1])