class Recipe:
    def __init__(self, params):
        self.name = params['name']
        self.description = params['description'] if 'description' in params else None
        self.products = params['products']
        self.nutritional_value = params['nutritional_value'] if 'nutritional_value' in params else None

    def to_json(self):
        return {
            "name": self.name,
            "description": self.description,
            "nutritional_value": self.nutritional_value,
            "products": self.products
        }
