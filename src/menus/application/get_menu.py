import inject
from ..domain.menu_database import MenuDatabase


class GetMenu:
    @inject.autoparams()
    def __init__(self, database: MenuDatabase):
        self.__database = database

    def execute(self, user, fromDate, toDate):
        if fromDate is None or toDate is None:
                response = []
        else:
            if user is None:
                response = self.__database.findByDate(user)
            else:
                response = self.__database.find(user, fromDate, toDate)
        return response
