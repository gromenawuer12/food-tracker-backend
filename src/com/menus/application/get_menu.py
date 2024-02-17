import inject

from ..domain.menu import get_monday_and_sunday
from ..domain.menu_database import MenuDatabase
from ...utils.log import Log


def check_param(dictionary, param):
    return param in dictionary and dictionary[param] != ''


class GetMenu:
    @inject.autoparams()
    def __init__(self, database: MenuDatabase, log: Log):
        self.__database = database
        self.log = log

    def execute(self, params=None):
        self.log.trace('GetMenu execute {0}', params)
        if params:
            if check_param(params, 'year_week') and check_param(params, 'username'):
                monday_and_sunday = get_monday_and_sunday(params['year_week'])
                return self.__database.find_by_user_between(params['username'], monday_and_sunday['monday_str'],
                                                            monday_and_sunday['sunday_str'])

            if check_param(params, 'year_week'):
                monday_and_sunday = get_monday_and_sunday(params['year_week'])
                return self.__database.find_all_between(monday_and_sunday['monday_str'],
                                                        monday_and_sunday['sunday_str'])

            if check_param(params, 'username'):
                return self.__database.find_by_username(params['username'])

        return self.__database.find_all()
