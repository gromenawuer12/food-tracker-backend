class Menu():
    def __init__(self, params):
        self.user = params['user']
        self.date = params['date']
        self.recipes = params['recipes']
        self.nutritional_value = params['nutritional_value']
        self.isLocked = False

    @property
    def nutritional_value(self):
        return self._nutritional_value

    @nutritional_value.setter
    def nutritional_value(self, nutritional_value):
        result = {}
        for index, elem in enumerate(nutritional_value):
            if elem[0] in result:
                result[elem[0]] = str(int(result[elem[0]]) + int(nutritional_value[index][2]))
            else:
                result[elem[0]] = nutritional_value[index][2]
        self._nutritional_value = result
