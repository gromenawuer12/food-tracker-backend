from types import SimpleNamespace

import inject
import json
from requests import Response

from ...application.add_weekly_menu import AddWeeklyMenu
from ...application.get_weekly_menu import GetWeeklyMenu
from ...domain.weekly_menu import WeeklyMenu
from ....resources.token.token_required_decorator import token_required

def resolve(event):
    weeklyMenusBlueprint = WeeklyMenusBlueprint()
    return eval({
                    "GET": "weeklyMenusBlueprint.get(pathParameters=event['pathParameters'], headers=event['headers'])",
                    "POST": "weeklyMenusBlueprint.post(headers=event['headers'], body=event['body'])"
                }[event['httpMethod']])

class WeeklyMenusBlueprint:
    @inject.autoparams()
    def __init__(self, get_weekly_menu: GetWeeklyMenu, add_weekly_menu: AddWeeklyMenu):
        self.get_weekly_menu = get_weekly_menu
        self.add_weekly_menu = add_weekly_menu

    # @weekly_menus_blueprint.route('/',methods=['GET'], defaults={'weeklyNumber': None})
    # @weekly_menus_blueprint.route('/<weeklyNumber>',methods=['GET'])
    @token_required
    def get(self, auth_username, pathParameters, headers) -> Response:
        weeklyNumber = pathParameters.get('weeklyNumber', None)
        return json.dumps(self.get_weekly_menu.execute(auth_username, weeklyNumber))

    # @weekly_menus_blueprint.route('/',methods=['POST'])
    @token_required
    def post(self, auth_username, headers, body) -> Response:
        return self.add_weekly_menu.execute(WeeklyMenu(json.loads(body, object_hook=lambda d: SimpleNamespace(**d).__dict__)))