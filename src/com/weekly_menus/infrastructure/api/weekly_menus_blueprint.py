from types import SimpleNamespace

import inject
import json

from ...application.add_weekly_menu import AddWeeklyMenu
from ...application.get_weekly_menu import GetWeeklyMenu
from ...domain.weekly_menu import WeeklyMenu
from ....resources.token.token_required_decorator import token_required
from ....utils.log import Log


def resolve(event):
    weekly_menus_blueprint = WeeklyMenusBlueprint()
    return {
        "GET": weekly_menus_blueprint.get,
        "POST": weekly_menus_blueprint.post
    }[event['httpMethod']](event=event)


class WeeklyMenusBlueprint:
    @inject.autoparams()
    def __init__(self, get_weekly_menu: GetWeeklyMenu, add_weekly_menu: AddWeeklyMenu, log: Log):
        log.trace('WeeklyMenusBlueprint - init')
        self.get_weekly_menu = get_weekly_menu
        self.add_weekly_menu = add_weekly_menu
        self.log = log

    @token_required
    def get(self, event):
        self.log.trace('WeeklyMenusBlueprint - get')
        query_string_parameters = event['queryStringParameters'];
        self.log.trace('WeeklyMenusBlueprint {0}', query_string_parameters)
        username = query_string_parameters.get('username', None)
        year_week = query_string_parameters.get('year_week', None)
        return self.get_weekly_menu.execute(username, year_week)

    @token_required
    def post(self, event):
        return self.add_weekly_menu.execute(
            WeeklyMenu(json.loads(event['body'], object_hook=lambda d: SimpleNamespace(**d).__dict__)))
