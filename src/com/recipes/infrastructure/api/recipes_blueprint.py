from types import SimpleNamespace
import inject, json
from ...application.add_recipe import AddRecipe
from ...application.get_recipe import GetRecipe
from ...application.delete_recipe import DeleteRecipe
from ...domain.recipe import Recipe
from ....resources.token.token_required_decorator import token_required


def resolve(event):
    recipes_blueprint = RecipesBlueprint()
    return {"GET": recipes_blueprint.get,
            "POST": recipes_blueprint.post,
            "DELETE": recipes_blueprint.delete
            }[event['httpMethod']](event=event)


class RecipesBlueprint:
    @inject.autoparams()
    def __init__(self, get_recipe: GetRecipe, add_recipe: AddRecipe, delete_recipe: DeleteRecipe):
        self.get_recipe = get_recipe
        self.add_recipe = add_recipe
        self.delete_recipe = delete_recipe

    @token_required
    def get(self, event):
        name = event['pathParameters'].get("name", None)
        return self.get_recipe.execute(name)

    @token_required
    def post(self, event):
        self.add_recipe.execute(Recipe(json.loads(event['body'], object_hook=lambda d: SimpleNamespace(**d).__dict__)))
        return {}

    @token_required
    def delete(self, event):
        body = json.loads(event['body'])
        name = body.get("name", None)
        self.delete_recipe.execute(name)
        return {}

    @token_required
    def modify(self, event):
        name = event['pathParameters'].get('name', None)
        if name is None:
            raise Exception
        recipe = self.get_recipe.execute(name)
        body = json.loads(event['body'])
        new_products = body.get("new_products", recipe["products"])
        new_name = body.get("new_name", recipe["name"])

        self.delete_recipe.execute(name)
        self.add_recipe.execute(Recipe(json.loads('{"name": new_name, "products": new_products}',
                                                  object_hook=lambda d: SimpleNamespace(**d).__dict__)))
        return {}
