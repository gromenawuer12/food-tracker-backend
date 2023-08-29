class Menu:
    def __init__(self, params):
        self.user = params['user']
        self.date = params['date']
        self.recipes = params['recipes']
        self.nutritional_value = params['nutritional_value']
        self.isLocked = False
