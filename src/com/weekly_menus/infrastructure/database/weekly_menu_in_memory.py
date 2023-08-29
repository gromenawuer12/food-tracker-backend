from ...domain.weekly_menu_database import WeeklyMenuDatabase
from ...domain.weekly_menu_exception import WeeklyMenuException


class WeeklyMenuInMemory(WeeklyMenuDatabase):
    def __init__(self):
        self.database = {}

    def create(self, weekly_menu):
        user = weekly_menu.user
        weekly_number = weekly_menu.weekly_number
        if (user + weekly_number) in self.database:
            raise WeeklyMenuException("There is a conflict to create this resource", 409)
        self.database[user + weekly_number] = weekly_menu
        return "Added"

    def find(self, user, weekly_number):
        out = []
        found = self.database.get(user + weekly_number)
        if found:
            for weekly_menu in found:
                out.push(weekly_menu)
        return out

    def update_nutritional_value(self, user, weekly_number, new_nutritional_value):
        self.database[user + weekly_number]['nutritional_value'] = new_nutritional_value
        return "Updated"
