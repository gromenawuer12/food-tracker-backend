class Recipe:
    def __init__(self, params):
        self.name = params['name']
        self.products = params['products']
        self.nutritional_values = []