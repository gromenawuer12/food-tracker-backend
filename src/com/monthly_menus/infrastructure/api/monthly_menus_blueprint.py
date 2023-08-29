import inject

from ...application.add_monthly_menu import AddMonthlyMenu
from ...application.get_monthly_menu import GetMonthlyMenu
from ....resources.token.token_required_decorator import token_required


def resolve(event):
    monthly_menus_blueprint = MonthlyMenusBlueprint()
    return {
        "GET": monthly_menus_blueprint.get,
    }[event['httpMethod']](event=event)


class MonthlyMenusBlueprint:
    @inject.autoparams()
    def __init__(self, get_monthly_menu: GetMonthlyMenu, add_monthly_menu: AddMonthlyMenu):
        self.get_monthly_menu = get_monthly_menu
        self.add_monthly_menu = add_monthly_menu

    @token_required
    def get(self, event):
        monthly_number = event.get('monthlyNumber', None)
        return self.get_monthly_menu.execute(event['auth_username'], monthly_number)
