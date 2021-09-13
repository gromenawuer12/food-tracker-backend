import inject
from ..domain.user import User
from ..domain.user_database import UserDatabase

class LoginUser:
    @inject.autoparams()
    def __init__(self, database: UserDatabase):
        self.__database = database

    def execute(self, username):
        return self.__database.find(username)
    