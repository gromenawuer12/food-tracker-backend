class NutritionalValue():
    def __init__(self, params):
        self.shortname = params['shortname']
        self.name = params['name']
        self.unit = params['unit']

    def to_json(self):
        return {"shortname": self.shortname, "name": self.name, "unit": self.unit}
