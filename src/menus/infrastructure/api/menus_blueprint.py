from types import SimpleNamespace
import inject, json, requests, jwt, datetime, os
from flask import Blueprint, Response, request
from ...application.add_menu import AddMenu
from ...application.get_menu import GetMenu
from ...application.delete_menu import DeleteMenu
from ...application.block_menu import BlockMenu
from ...domain.menu import Menu
from resources.token.token_required_decorator import token_required
from datetime import date


@inject.autoparams()
def create_menus_blueprint(get_menu: GetMenu, add_menu: AddMenu, delete_menu: DeleteMenu, block_menu: BlockMenu) -> Blueprint:
    menus_blueprint = Blueprint('menus', __name__)

    @menus_blueprint.route('/',methods=['GET'], defaults={'user': None,'date':None})
    @menus_blueprint.route('/<user>',methods=['GET'], defaults={'date':None})
    @menus_blueprint.route('/<user>/<date>',methods=['GET'], defaults={'user':None})
    @token_required
    def get(auth_username,user, date) -> Response:
        return json.dumps(get_menu.execute(user, date))

    @menus_blueprint.route('/',methods=['POST'])
    @token_required
    def post(auth_username) -> Response:
        token = jwt.encode({'username': auth_username, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30),}, os.getenv('SECRET_KEY'),algorithm="HS256")
        response = request.get_json()
        recipes = response.get("recipes")
        products = []
        nutritional_value = []
        for recipe in recipes:
            products+=json.loads(requests.get(os.getenv('ENDPOINT_URL')+'recipes/'+recipe,headers={'Authorization': 'access_token '+token}).content.decode("utf-8")).get("products")
        for product in products:
            nutritional_value.append(json.loads(requests.get(os.getenv('ENDPOINT_URL')+'products/'+product[0],headers={'Authorization': 'access_token '+token}).content.decode("utf-8")).get("nutritional_value"))
        response["nutritional_value"] = nutritional_value
        return add_menu.execute(Menu(json.loads(json.dumps(response),object_hook=lambda d: SimpleNamespace(**d).__dict__)))
    
    @menus_blueprint.route('/',methods=['DELETE'])
    @token_required
    def delete(auth_username) -> Response:
        if request.get_json().get("user"):
            user = request.get_json().get("user")
        else:
            user = auth_username
        return delete_menu.execute(user,request.get_json().get("date"))

    @menus_blueprint.route('/block',methods=['GET'])
    @token_required
    def block(auth_username) -> Response:
        return json.dumps(block_menu.execute(auth_username,date.today().strftime("%Y-%m-%d")))
        
    return menus_blueprint