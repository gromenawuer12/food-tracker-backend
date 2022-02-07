import inject
from ..domain.menu_database import MenuDatabase

class GetMenu:
    @inject.autoparams()
    def __init__(self, database: MenuDatabase):
        self.__database = database

    """
    check to delete unnecessary database methods
    """
    def execute(self, user, date):
        if user is None and date is None:
            response = self.__database.findAll()
        elif user is None and date is not None:
            response = self.__database.findByDate(date)
        elif user is not None and date is None:
            response = self.__database.findByUser(user)
        else:
            response = self.__database.find(user, date)
        return response