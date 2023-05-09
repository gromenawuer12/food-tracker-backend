from types import SimpleNamespace
import inject, json, jwt, datetime, os
from requests import Response
from ...application.add_menu import AddMenu
from ...application.get_menu import GetMenu
from ...application.delete_menu import DeleteMenu
from ...application.block_menu import BlockMenu
from ...domain.menu import Menu
from ....resources.token.token_required_decorator import token_required
from datetime import date
from ....products.infrastructure.api.products_blueprint import ProductsBlueprint
from ....recipes.infrastructure.api.recipes_blueprint import RecipesBlueprint

def resolve(event):
    menusBlueprint = MenusBlueprint()
    return eval({
                    "GET": "menusBlueprint.get(headers=event['headers'], queryStringParameters=event['queryStringParameters'])",
                    "POST": "menusBlueprint.post(headers=event['headers'], body=event['body'])",
                    "DELETE": "menusBlueprint.delete(headers=event['headers'], body=event['body'])"
                }[event['httpMethod']])
class MenusBlueprint:
    @inject.autoparams()
    def __init__(self, get_menu: GetMenu, add_menu: AddMenu, delete_menu: DeleteMenu, block_menu: BlockMenu):
        self.get_menu = get_menu
        self.add_menu = add_menu
        self.delete_menu = delete_menu
        self.block_menu = block_menu

    # @menus_blueprint.route('/',methods=['GET'], defaults={'user': None,'date':None})
    # @menus_blueprint.route('/<user>',methods=['GET'], defaults={'date':None})
    # @menus_blueprint.route('/<user>/<date>',methods=['GET'], defaults={'user':None})
    @token_required
    def get(self, auth_username, queryStringParameters, headers) -> Response:
        user = queryStringParameters.get('user', None)
        fromDate = queryStringParameters.get('from', None)
        toDate = queryStringParameters.get('to', None)

        return self.get_menu.execute(user, fromDate, toDate)

    # @menus_blueprint.route('/',methods=['POST'])
    @token_required
    def post(self, auth_username, body, headers) -> Response:
        response = json.loads(body)
        recipes = response.get("recipes")
        products = []
        nutritional_value = []
        recipesBlueprint = RecipesBlueprint()
        productsBlueprint = ProductsBlueprint()
        for recipe in recipes:
            products += json.loads(recipesBlueprint.get(queryStringParameters={"name": recipe}, headers=headers)).get("products")
        for product in products:
            nutritional_value += json.loads(productsBlueprint.get(queryStringParameters={"name": product[0]}, headers=headers)).get("nutritional_value")
        response["nutritional_value"] = nutritional_value
        return self.add_menu.execute(Menu(json.loads(json.dumps(response), object_hook=lambda d: SimpleNamespace(**d).__dict__)))
    
    # @menus_blueprint.route('/',methods=['DELETE'])
    @token_required
    def delete(self, auth_username, body, headers) -> Response:
        body = json.loads(body)
        user = body.get("user", auth_username)
        return self.delete_menu.execute(user, body.get("date"))

    # @menus_blueprint.route('/block',methods=['GET'])
    @token_required
    def block(self, auth_username, headers) -> Response:
        return json.dumps(self.block_menu.execute(auth_username, date.today().strftime("%Y-%m-%d")))