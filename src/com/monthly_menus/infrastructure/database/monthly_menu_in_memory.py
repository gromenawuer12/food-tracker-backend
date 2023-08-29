from ...domain.monthly_menu_database import MonthlyMenuDatabase
from ...domain.monthly_menu_exception import MonthlyMenuException


class MonthlyMenuInMemory(MonthlyMenuDatabase):
    def __init__(self):
        self.database = {}

    def create(self, weekly_menu):
        user = weekly_menu.user
        weekly_number = weekly_menu.weekly_number
        if (user + weekly_number) in self.database:
            raise MonthlyMenuException("There is a conflict to create this resource", 409)
        self.database[user + weekly_number] = weekly_menu
        return "Added"

    def find(self, user, monthly_number):
        out = []
        found = self.database.get(user + monthly_number)
        if found:
            for monthly_menu in found:
                out.push(monthly_menu)
        return out

    def update_nutritional_value(self, user, weekly_number, new_nutritional_value):
        self.database[user + weekly_number]['nutritional_value'] = new_nutritional_value
        return "Updated"
