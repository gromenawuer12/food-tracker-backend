from .user_exception import UserException
import bcrypt
import re


class User():
    def __init__(self, params):
        self.username = params['username']
        self.password = params['password']
        self.role = params['role']

    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, username):
        if re.search(r"\W", username):
            raise UserException('Username can only contain alphanumeric values and low slashes', 400)
        self._username = username

    @username.deleter
    def username(self):
        del (self._username)

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, password):
        self._password = bcrypt.hashpw(password, bcrypt.gensalt(10))

    @password.deleter
    def password(self):
        del self._password
