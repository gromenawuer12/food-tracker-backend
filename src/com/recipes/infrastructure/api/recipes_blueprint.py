import inject, json
from ...application.add_recipe import AddRecipe
from ...application.edit_recipe import EditRecipe
from ...application.get_recipe import GetRecipe
from ...application.delete_recipe import DeleteRecipe
from ...domain.recipe import Recipe
from ....resources.token.token_required_decorator import token_required
from ....utils.log import Log


def resolve(event):
    recipes_blueprint = RecipesBlueprint()
    return {"GET": recipes_blueprint.get,
            "POST": recipes_blueprint.post,
            "PUT": recipes_blueprint.put,
            "DELETE": recipes_blueprint.delete
            }[event['httpMethod']](event=event)


class RecipesBlueprint:
    @inject.autoparams()
    def __init__(self, get_recipe: GetRecipe, add_recipe: AddRecipe, delete_recipe: DeleteRecipe,
                 edit_recipe: EditRecipe, log: Log):
        self.get_recipe = get_recipe
        self.add_recipe = add_recipe
        self.edit_recipe = edit_recipe
        self.delete_recipe = delete_recipe
        self.log = log

    @token_required
    def get(self, event):
        name = event['pathParameters'].get("name", None)
        return self.get_recipe.execute(name)

    @token_required
    def post(self, event):
        body = json.loads(event['body'])
        self.log.trace('post: body={0}', body)
        self.add_recipe.execute(Recipe(body))

    @token_required
    def delete(self, event):
        body = json.loads(event['body'])
        name = body.get("name", None)
        self.delete_recipe.execute(name)
        return {}

    @token_required
    def put(self, event):
        self.log.debug('put: proxy={0}', json.dumps(event['pathParameters']['proxy']))
        name = event['pathParameters']['proxy'].split('/')[1]
        self.log.trace('put: shortname={0}', name)

        if name is None:
            raise Exception

        body = json.loads(event['body'])
        self.log.trace('put: body={0}', body)

        self.edit_recipe.execute(name, Recipe(body))
