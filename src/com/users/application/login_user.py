import hashlib

import inject

from ..domain.user_database import UserDatabase
from ..infrastructure.api.login_exception import LoginException
from ...utils.log import Log


def hash_password(password):
    password_bytes = password.encode('utf-8')
    hash_object = hashlib.sha256(password_bytes)
    return hash_object.hexdigest()


class LoginUser:
    @inject.autoparams()
    def __init__(self, database: UserDatabase, log: Log):
        self.__database = database
        self.log = log

    def execute(self, username, password):
        user = self.__database.find(username)
        self.log.trace('LoginUser {0}', hash_password(password))

        if user is None or not user['password'] == hash_password(password):
            raise LoginException("Invalid username or password")

        return user
