from types import SimpleNamespace
import inject, json
from flask import Blueprint, Response, request
from ...application.add_weekly_menu import AddWeeklyMenu
from ...application.get_weekly_menu import GetWeeklyMenu
from ...domain.weekly_menu import WeeklyMenu
from resources.token.token_required_decorator import token_required

@inject.autoparams()
def create_weekly_menus_blueprint(get_weekly_menu: GetWeeklyMenu, add_weekly_menu: AddWeeklyMenu) -> Blueprint:
    weekly_menus_blueprint = Blueprint('weekly_menus', __name__)

    @weekly_menus_blueprint.route('/',methods=['GET'], defaults={'weeklyNumber': None})
    @weekly_menus_blueprint.route('/<weeklyNumber>',methods=['GET'])
    @token_required
    def get(auth_username, weeklyNumber) -> Response:
        return json.dumps(get_weekly_menu.execute(auth_username, weeklyNumber))

    @weekly_menus_blueprint.route('/',methods=['POST'])
    @token_required
    def post(auth_username) -> Response:
        return add_weekly_menu.execute(WeeklyMenu(json.loads(json.dumps(request.get_json()),object_hook=lambda d: SimpleNamespace(**d).__dict__)))
    
    return weekly_menus_blueprint