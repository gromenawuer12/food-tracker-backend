class Product():
    def __init__(self, params):
        self.name = params['name']
        self.nutritional_value = params['nutritional_value']
        self.description = params['description'] if 'description' in params else None
        self.supermarket = params['supermarket'] if 'supermarket' in params else None

    def to_json(self):
        return {
            "name": self.name,
            "description": self.description,
            "supermarket": self.supermarket,
            "nutritional_value": self.nutritional_value
        }
