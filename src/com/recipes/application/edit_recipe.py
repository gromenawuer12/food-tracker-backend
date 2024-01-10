import inject

from .add_recipe import AddRecipe
from ..domain.recipe import Recipe
from ..domain.recipe_database import RecipeDatabase
from ..domain.recipe_exception import RecipeException
from ...utils.log import Log


class EditRecipe:
    @inject.autoparams()
    def __init__(self, database: RecipeDatabase, add_recipe: AddRecipe, log: Log):
        self.__database = database
        self.__add_recipe = add_recipe
        self.__log = log

    def execute(self, name, recipe: Recipe):
        recipe_old = Recipe(self.__database.find(name))
        self.__log.trace('EditRecipe: recipe={0}', recipe_old.to_json())

        self.__database.delete(name)
        self.__log.trace('EditRecipe: recipe with name={0} deleted', name)
        try:
            self.__log.trace('EditRecipe: creating recipe={0}', recipe.to_json())
            self.__add_recipe.execute(recipe)
        except RecipeException as product_exception:
            self.__log.error('EditRecipe: error while adding, restoring to {0}', recipe_old.to_json())
            self.__database.create(recipe_old)
            raise product_exception
