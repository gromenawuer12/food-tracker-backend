import inject

from ..domain.menu import get_monday_and_sunday
from ..domain.menu_database import MenuDatabase


class GetMenu:
    @inject.autoparams()
    def __init__(self, database: MenuDatabase):
        self.__database = database

    def execute(self, params=None):
        if params:
            if 'year_week' in params and params['year_week'] is not None and 'username' in params:
                monday_and_sunday = get_monday_and_sunday(params['year_week'])
                return self.__database.find_between(params['username'], monday_and_sunday['monday_str'],
                                                    monday_and_sunday['sunday_str'])

            if 'year_week' in params and params['year_week'] is not '':
                monday_and_sunday = get_monday_and_sunday(params['year_week'])
                return self.__database.find_from_to(monday_and_sunday['monday_str'], monday_and_sunday['sunday_str'])

        return self.__database.find_all()
