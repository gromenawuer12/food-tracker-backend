import inject
from ..domain.recipe_database import RecipeDatabase


class GetRecipe:
    @inject.autoparams()
    def __init__(self, database: RecipeDatabase):
        self.__database = database

    def execute(self, name):
        if name is None:
            response = self.__database.find_all()
        else:
            response = self.__database.find(name)
        return response
