import datetime


def get_week_number(date_time):
    iso_calendar = date_time.isocalendar()
    return str(iso_calendar[0]) + "-" + str(iso_calendar[1])


class WeeklyMenu():
    def __init__(self, params, date=None):
        if params:
            self.username = params['username']
            self.weekly_number = params['date']
            self.menus = {params['date']: params['menu']}
            self.menu = params['menu']

            nutritional_value_dict = {}
            for nutritional_value_element in params['nutritional_value']:
                nutritional_value_dict[nutritional_value_element['name']] = nutritional_value_element
            self.nutritional_value = nutritional_value_dict
        else:
            self.username = None
            self.weekly_number = date
            self.menus = {}
            self.menu = None
            self.nutritional_value = {}

    @property
    def weekly_number(self):
        return self._weekly_number

    @weekly_number.setter
    def weekly_number(self, weekly_number):
        aux_date = datetime.datetime.strptime(weekly_number, "%Y-%m-%d")
        self._weekly_number = get_week_number(aux_date)

    def to_json(self):
        return {
            "username": self.username,
            "menus": self.menus,
            "weekly_number": self.weekly_number,
            'nutritional_value': self.nutritional_value
        }
