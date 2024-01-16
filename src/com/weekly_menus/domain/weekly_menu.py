import datetime


class WeeklyMenu():
    def __init__(self, params):
        self.username = params['username']
        self.weekly_number = params['date']
        self.menus = [params['menu']]

        nutritional_value_dict = {}
        for nutritional_value_element in params['nutritional_value']:
            nutritional_value_dict[nutritional_value_element['name']] = nutritional_value_element
        self.nutritional_value = nutritional_value_dict

    @property
    def weekly_number(self):
        return self._weekly_number

    @weekly_number.setter
    def weekly_number(self, weekly_number):
        aux_date = datetime.datetime.strptime(weekly_number, "%Y-%m-%d")
        aux_tuple = datetime.date(aux_date.year, aux_date.month, aux_date.day).isocalendar()
        self._weekly_number = str(aux_tuple[0]) + "-" + str(aux_tuple[1])

    def to_json(self):
        return {
            "username": self.username,
            "menus": self.menus,
            "weekly_number": self.weekly_number,
            'nutritional_value': self.nutritional_value
        }