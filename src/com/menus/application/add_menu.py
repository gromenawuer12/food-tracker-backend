import inject
from ..domain.menu import Menu
from ..domain.menu_database import MenuDatabase
from ...recipes.application.add_recipe import AddRecipe
from ...recipes.application.delete_recipe import DeleteRecipe
from ...recipes.application.get_recipe import GetRecipe
from ...recipes.domain.recipe import Recipe


class AddMenu:
    @inject.autoparams()
    def __init__(self, database: MenuDatabase, get_recipe: GetRecipe, delete_recipe: DeleteRecipe,
                 add_recipe: AddRecipe):
        self.__database = database
        self.__get_recipe = get_recipe
        self.__delete_recipe = delete_recipe
        self.__add_recipe = add_recipe

    def execute(self, user, date, recipeNames):
        nutritional_values = {}

        for recipeName in recipeNames:
            recipe = self.__get_recipe.execute(recipeName)
            if 'nutritional_values' not in recipe:
                self.__delete_recipe.execute(recipe['name'])
                self.__add_recipe.execute(Recipe(recipe))
                recipe = self.__get_recipe.execute(recipe['name'])
            for nutritional_value in recipe['nutritional_values']:
                if nutritional_value in nutritional_values:
                    nutritional_values[nutritional_value] = str(float(
                        nutritional_values[nutritional_value]) + float(
                        recipe['nutritional_values'][nutritional_value]['value']))
                else:
                    nutritional_values[nutritional_value] = recipe['nutritional_values'][nutritional_value]['value']

        menu = Menu({
            'user': user,
            'date': date,
            'recipes': recipeNames,
            'nutritional_value': nutritional_values
        })

        self.__database.create(menu)
