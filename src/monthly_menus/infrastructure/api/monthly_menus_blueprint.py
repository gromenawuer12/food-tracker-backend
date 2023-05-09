from types import SimpleNamespace
import inject, json
from requests import Response
from ...application.add_monthly_menu import AddMonthlyMenu
from ...application.get_monthly_menu import GetMonthlyMenu
from ...domain.monthly_menu import MonthlyMenu
from ....resources.token.token_required_decorator import token_required

def resolve(event):
    monthlyMenusBlueprint = MonthlyMenusBlueprint()
    return eval({
                    "GET": "monthlyMenusBlueprint.get(queryStringParameters=event['queryStringParameters'], headers=event['headers'])",
                    "POST": "monthlyMenusBlueprint.post(headers=event['headers'], body=event['body'])"
                }[event['httpMethod']])

class MonthlyMenusBlueprint:
    @inject.autoparams()
    def __init__(self, get_monthly_menu: GetMonthlyMenu, add_monthly_menu: AddMonthlyMenu):
        self.get_monthly_menu = get_monthly_menu
        self.add_monthly_menu = add_monthly_menu

    @token_required
    def get(self, auth_username, queryStringParameters, headers) -> Response:
        monthlyNumber = queryStringParameters.get('monthlyNumber', None)
        return json.dumps(self.get_monthly_menu.execute(auth_username, monthlyNumber))

    @token_required
    def post(self, auth_username, headers, body) -> Response:
        return self.add_monthly_menu.execute(
            MonthlyMenu(json.loads(body, object_hook=lambda d: SimpleNamespace(**d).__dict__)))
