import inject

from ..domain.settings import Settings
from ..domain.settings_database import SettingsDatabase
from ..domain.settings_exception import SettingsException
from ...utils.log import Log


class AddSettings:
    @inject.autoparams()
    def __init__(self, database: SettingsDatabase, log: Log):
        self.__database = database
        self.__log = log

    def execute(self, settings: Settings):
        self.__log.trace('AddSettings: settings={0}', settings.to_json())
        try:
            settings_old = Settings(self.__database.find(settings.shortname))
        except SettingsException:
            self.__database.create(settings)
            return
        self.__log.trace('AddSettings: settings={0}', settings_old.to_json())

        self.__database.delete(settings.shortname)
        self.__log.trace('AddSettings: settings with name={0} deleted', settings.shortname)
        try:
            self.__log.trace('AddSettings: creating settings={0}', settings.to_json())
            self.__database.create(settings)
        except SettingsException as settings_exception:
            self.__log.error('AddSettings: error while adding, restoring to {0}', settings_old.to_json())
            self.__database.create(settings_old)
            raise settings_exception
