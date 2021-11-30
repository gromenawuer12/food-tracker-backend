import inject
from ..domain.recipe import Recipe
from ..domain.recipe_database import RecipeDatabase

class AddRecipe:
    @inject.autoparams()
    def __init__(self, database: RecipeDatabase):
        self.__database = database

    def execute(self, recipe: Recipe) -> str:
        self.__database.create(recipe)
        return "Added"