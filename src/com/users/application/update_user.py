import inject
from ..domain.user_database import UserDatabase

class UpdateUser:
    @inject.autoparams()
    def __init__(self, database: UserDatabase):
        self.__database = database

    def execute(self, username, password, role) -> str:
        self.__database.update(username, password, role)
        return "Updated"