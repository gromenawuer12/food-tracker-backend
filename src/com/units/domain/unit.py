class Unit:
    def __init__(self, params):
        self.shortname = params['shortname']
        self.name = params['name']

    def to_json(self):
        return {"shortname": self.shortname, "name": self.name}
