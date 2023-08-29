from ...domain.user_exception import UserException
from ...domain.user_database import UserDatabase


class UserInMemory(UserDatabase):
    def __init__(self):
        self.database = {"John": {"username": "John", "role": "admin", "password": "eee"},
                         "Pepito": {"username": "Pepito", "role": "user", "password": "aaa"},
                         "test": {"username": "test",
                                  "password": "JDJiJDEwJDkzTnhoYUFWSnRSYjJtWkZ4Llcyd09YWTNrcFVpQTAzeXA4OHdpTk9RTDkuLkFiSmFIREY2",
                                  "role": "test"}}

    def create(self, user):
        if user.username in self.database:
            raise UserException("There is a conflict to create this resource", 409)
        self.database[user.username] = {"username": user.username, "password": user.password, "role": user.role}
        return "Added"

    def find(self, username):
        return self.database.get(username)

    def update(self, username, password, role):
        self.database[username]["role"] = role
        self.database[username]["password"] = password
        return "Updated"
