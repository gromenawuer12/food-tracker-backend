from ...domain.unit_database import UnitDatabase


class UnitInMemory(UnitDatabase):
    def __init__(self):
        self.database = {}

    def create(self, unit):
        self.database[unit.shortname] = unit
        return "Added"

    def find_all(self):
        return [{key: value} for key, value in self.database.items()]

    def find(self, shortname):
        return self.database[shortname]

    def delete(self, shortname):
        del self.database[shortname]
        return "Deleted"
