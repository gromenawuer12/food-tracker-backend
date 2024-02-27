class Settings:
    def __init__(self, params):
        self.shortname = params['shortname'] if 'shortname' in params else params['SK']
        self.parts_of_day = params['partsOfDay'] if 'partsOfDay' in params else params['settings']['partsOfDay']

    def serialize(self):
        return {"shortname": self.shortname, "partsOfDay": self.parts_of_day}

    def to_json(self):
        return {"shortname": self.shortname, "parts_of_day": self.parts_of_day}
