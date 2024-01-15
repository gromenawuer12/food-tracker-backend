def get_is_locked(params):
    if 'isLocked' not in params:
        return False

    if params['isLocked'] == 'false':
        return False

    return True


class Menu:
    def __init__(self, params):
        self.username = params['username']
        self.date = params['date']
        self.recipes = params['recipes']
        self.nutritional_value = params['nutritional_value'] if 'nutritional_value' in params else []
        self.isLocked = get_is_locked(params)

    def to_json(self):
        return {
            "username": self.username,
            "date": self.date,
            'isLocked': self.isLocked,
            "recipes": self.recipes,
            'nutritional_value': self.nutritional_value
        }
