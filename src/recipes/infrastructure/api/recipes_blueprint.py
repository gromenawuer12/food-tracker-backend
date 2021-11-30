from types import SimpleNamespace
import inject, json
from flask import Blueprint, Response, request
from ...application.add_recipe import AddRecipe
from ...application.get_recipe import GetRecipe
from ...application.delete_recipe import DeleteRecipe
from ...domain.recipe import Recipe
from resources.token.token_required_decorator import token_required


@inject.autoparams()
def create_recipes_blueprint(get_recipe: GetRecipe, add_recipe: AddRecipe, delete_recipe: DeleteRecipe) -> Blueprint:
    recipes_blueprint = Blueprint('recipes', __name__)

    @recipes_blueprint.route('/',methods=['GET'], defaults={'name': None})
    @recipes_blueprint.route('/<name>',methods=['GET'])
    @token_required
    def get(auth_username,name) -> Response:
        return json.dumps(get_recipe.execute(name))

    @recipes_blueprint.route('/',methods=['POST'])
    @token_required
    def post(auth_username) -> Response:
        return add_recipe.execute(Recipe(json.loads(json.dumps(request.get_json()),object_hook=lambda d: SimpleNamespace(**d).__dict__)))
    
    @recipes_blueprint.route('/',methods=['DELETE'])
    @token_required
    def delete(auth_username) -> Response:
        return delete_recipe.execute(request.get_json().get("name"))

    return recipes_blueprint