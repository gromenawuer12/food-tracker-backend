import hashlib
from datetime import date, timedelta

import inject

from ..domain.user_database import UserDatabase
from ..infrastructure.api.login_exception import LoginException
from ...menus.application.block_menu import BlockMenu
from ...utils.log import Log


def hash_password(password):
    password_bytes = password.encode('utf-8')
    hash_object = hashlib.sha256(password_bytes)
    return hash_object.hexdigest()


class LoginUser:
    @inject.autoparams()
    def __init__(self, database: UserDatabase, block_menu: BlockMenu, log: Log):
        self.__database = database
        self.__block_menu = block_menu
        self.log = log

    def execute(self, username, password):
        user = self.__database.find(username)
        self.log.trace('LoginUser')

        if user is None or not user['password'] == hash_password(password):
            raise LoginException("Invalid username or password")

        self.log.trace('Blocking menu')
        self.__block_menu.execute(username, (date.today() - timedelta(days=9)).strftime("%Y-%m-%d"))
        self.log.trace('Menu blocked')

        return user
