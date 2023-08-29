import inject
from ..domain.recipe import Recipe
from ..domain.recipe_database import RecipeDatabase

class DeleteRecipe:
    @inject.autoparams()
    def __init__(self, database: RecipeDatabase):
        self.__database = database

    def execute(self, name) -> str:
        self.__database.delete(name)