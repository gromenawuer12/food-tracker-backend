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
        for d in nutritional_value:
            for elem in d:
                if elem in result:
                    result[elem]=str(int(result[elem])+int(d[elem]))
                else:
                    result[elem]=d[elem]
        self._nutritional_value = result