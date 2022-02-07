from types import SimpleNamespace
import inject, json
from flask import Blueprint, Response, request
from ...application.add_monthly_menu import AddMonthlyMenu
from ...application.get_monthly_menu import GetMonthlyMenu
from ...domain.monthly_menu import MonthlyMenu
from resources.token.token_required_decorator import token_required

@inject.autoparams()
def create_monthly_menus_blueprint(get_monthly_menu: GetMonthlyMenu, add_monthly_menu: AddMonthlyMenu) -> Blueprint:
    monthly_menus_blueprint = Blueprint('monthly_menus', __name__)

    @monthly_menus_blueprint.route('/',methods=['GET'], defaults={'monthlyNumber': None})
    @monthly_menus_blueprint.route('/<monthlyNumber>',methods=['GET'])
    @token_required
    def get(auth_username, monthlyNumber) -> Response:
        return json.dumps(get_monthly_menu.execute(auth_username, monthlyNumber))

    @monthly_menus_blueprint.route('/',methods=['POST'])
    @token_required
    def post(auth_username) -> Response:
        return add_monthly_menu.execute(MonthlyMenu(json.loads(json.dumps(request.get_json()),object_hook=lambda d: SimpleNamespace(**d).__dict__)))
    
    return monthly_menus_blueprint