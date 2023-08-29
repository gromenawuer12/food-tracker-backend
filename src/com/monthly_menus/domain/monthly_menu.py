

class MonthlyMenu:
    def __init__(self, params):
        self.user = params['user']
        self.monthly_number = params['date']
        self.nutritional_value = params['nutritional_value']

    @property
    def monthly_number(self):
        return self._monthly_number

    @monthly_number.setter
    def monthly_number(self, monthly_number):
        self._monthly_number = monthly_number[0:7]
