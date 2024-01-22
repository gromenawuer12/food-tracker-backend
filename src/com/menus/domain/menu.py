import datetime


def get_monday_and_sunday(year_week):
    monday = datetime.datetime.strptime(year_week + '-1', "%Y-W%W-%w")
    sunday = (monday + datetime.timedelta(days=6))

    return {'monday_str': monday.strftime('%Y-%m-%d'),
            'sunday_str': sunday.strftime('%Y-%m-%d')}


class Menu:
    def __init__(self, params):
        self.username = params['username']
        self.date = params['date']
        self.recipes = params['recipes'] if 'recipes' in params else []
        self.products = params['products'] if 'products' in params else []
        self.nutritional_value = params['nutritional_value'] if 'nutritional_value' in params else []

    def to_json(self):
        return {
            "username": self.username,
            "date": self.date,
            "recipes": self.recipes,
            'nutritional_value': self.nutritional_value
        }
