import inject
from ..domain.user import User
from ..domain.user_database import UserDatabase


class AddUser:
    @inject.autoparams()
    def __init__(self, database: UserDatabase):
        self.__database = database

    def execute(self, user: User) -> str:
        self.__database.create(user)
        return "Added"
