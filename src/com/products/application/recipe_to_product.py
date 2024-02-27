import inject

from ..domain.product import Product
from ..domain.product_database import ProductDatabase
from ...recipes.application.get_recipe import GetRecipe
from ...utils.log import Log


class RecipeToProduct:
    @inject.autoparams()
    def __init__(self, database: ProductDatabase, get_recipe: GetRecipe, log: Log):
        self.__database = database
        self.__get_recipe = get_recipe
        self.__log = log

    def execute(self, recipe_name, portions):
        recipe = self.__get_recipe.execute(recipe_name)
        nutritional_value_calculated = []
        for nutritional_value_component in recipe['nutritional_value']:
            self.__log.trace("-->RecipeToProduct nutritional_value_component: {0}", nutritional_value_component)
            nutritional_value_calculated.append(
                [
                    nutritional_value_component['name'],
                    nutritional_value_component['unit'],
                    str(round(float(nutritional_value_component['value']) / int(portions), 2)),
                ]
            )

        product = Product({
            "name": recipe_name,
            "description": recipe['description'],
            "nutritional_value": nutritional_value_calculated,
            "recipe_name": recipe_name
        })
        self.__database.create(product)
