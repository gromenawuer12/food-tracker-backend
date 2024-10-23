import inject

from ..domain.settings_database import SettingsDatabase


class GetSettings:
    @inject.autoparams()
    def __init__(self, database: SettingsDatabase):
        self.__database = database

    def execute(self, shortname):
        if shortname is None:
            response = self.__database.find_all()
        else:
            response = self.__database.find(shortname)
        return response.serialize()
