from types import SimpleNamespace
import inject, json
from requests import Response
from ...application.add_recipe import AddRecipe
from ...application.get_recipe import GetRecipe
from ...application.delete_recipe import DeleteRecipe
from ...domain.recipe import Recipe
from ....resources.token.token_required_decorator import token_required


def resolve(event):
    recipesBlueprint = RecipesBlueprint()
    return eval({
                    "GET": "recipesBlueprint.get(headers=event['headers'], queryStringParameters=event['queryStringParameters'])",
                    "POST": "recipesBlueprint.post(headers=event['headers'], body=event['body'])",
                    "DELETE": "recipesBlueprint.delete(headers=event['headers'], body=event['body'])"
                }[event['httpMethod']])


class RecipesBlueprint:
    @inject.autoparams()
    def __init__(self, get_recipe: GetRecipe, add_recipe: AddRecipe, delete_recipe: DeleteRecipe):
        self.get_recipe = get_recipe
        self.add_recipe = add_recipe
        self.delete_recipe = delete_recipe

    # @recipes_blueprint.route('/',methods=['GET'], defaults={'name': None})
    # @recipes_blueprint.route('/<name>',methods=['GET'])
    @token_required
    def get(self, auth_username, queryStringParameters, headers) -> Response:
        name = queryStringParameters.get("name", None)
        return json.dumps(self.get_recipe.execute(name))

    # @recipes_blueprint.route('/',methods=['POST'])
    @token_required
    def post(self, auth_username, body, headers) -> Response:
        return self.add_recipe.execute(Recipe(json.loads(body, object_hook=lambda d: SimpleNamespace(**d).__dict__)))

    # @recipes_blueprint.route('/',methods=['DELETE'])
    @token_required
    def delete(self, auth_username, body, headers) -> Response:
        body = json.loads(body)
        name = body.get("name", None)
        return self.delete_recipe.execute(name)

    @token_required
    def modify(self, auth_username, queryStringParameters, headers, body) -> Response:
        name = queryStringParameters.get('name', None)
        if name is None:
            raise Exception
        recipe = self.get_recipe.execute(name)
        body = json.loads(body)
        new_products = body.get("new_products", recipe["products"])
        new_name = body.get("new_name", recipe["name"])

        self.delete_recipe.execute(name)
        self.add_recipe.execute(Recipe(json.loads('{"name": new_name, "products": new_products}', object_hook=lambda d: SimpleNamespace(**d).__dict__)))
        return {}
