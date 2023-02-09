import inject

from ..domain.user import User
from ..domain.user_database import UserDatabase
from ..domain.user_permissions import delete_attrs


class GetUser:
    @inject.autoparams()
    def __init__(self, database: UserDatabase):
        self.__database = database

    def execute(self, username, auth_username):
        user = self.__database.find(username)
        user = User(user)
        if auth_username is None:
            return delete_attrs(user, ["_password", "role"])
        if username != auth_username:
            return delete_attrs(user, ["_password"])
        return user
