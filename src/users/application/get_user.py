import inject

from ..domain.user import User
from ..domain.user_database import UserDatabase
from ..domain.user_permissions import delete_attrs


class GetUser:
    @inject.autoparams()
    def __init__(self, database: UserDatabase):
        self.__database = database

    def execute(self):
        return self.__database.findAll()
