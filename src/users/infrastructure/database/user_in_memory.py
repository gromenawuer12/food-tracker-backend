from users.domain.user_exception import UserException
from ...domain.user_database import UserDatabase
import sys

class UserInMemory(UserDatabase):
    def __init__(self):
        self.database = {"John":{"username":"John","role":"admin","password":"eee"},
        "Pepito":{"username":"Pepito","role":"user","password":"aaa"},
        "test":{"username":"test","password":"sha256$3xOARts1mLQGVSBk$02ffdf6493fbeb6259ec11cdd411907da0282224cde41306dffe1bb912ef1214","role":"test"}}

    def create(self, user):
        if user.username in self.database:
            raise UserException("There is a conflict to create this resource",409)
        self.database[user.username] = {"username":user.username,"password":user.password,"role":user.role}
        return "Added"

    def find(self, username):
        return self.database.get(username)
    
    def update(self, username, password, role):
        self.database[username]["role"] = role
        self.database[username]["password"] = password
        return "Updated"