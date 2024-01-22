def str_sum(value1, value2):
    return str(round(float(value1) + float(value2), 2))


class NutritionalValue:
    def __init__(self, params):
        self.shortname = params['shortname']
        self.name = params['name']
        self.unit = params['unit']

    def to_json(self):
        return {"shortname": self.shortname, "name": self.name, "unit": self.unit}
