import json
from types import SimpleNamespace

import inject
from ..domain.recipe import Recipe
from ..domain.recipe_database import RecipeDatabase
from ...products.application.get_product import GetProduct


class AddRecipe:
    @inject.autoparams()
    def __init__(self, database: RecipeDatabase, get_product: GetProduct):
        self.__database = database
        self.__get_product = get_product

    def __calculate(self, other, grams, value):
        return str(float(other) + (float(value) * float(grams) / 100))

    def execute(self, recipe: Recipe):
        print(recipe)
        nutritional_values_calculated = {}
        products = recipe.products
        for product in products:
            nutritional_values = self.__get_product.execute(product[0])['nutritional_value']
            for nutritional_value in nutritional_values:
                if nutritional_value[0] not in nutritional_values_calculated:
                    nutritional_values_calculated[nutritional_value[0]] = \
                        {'unit': nutritional_value[1],
                         'value': self.__calculate(0, product[2], nutritional_value[2]),
                         'name': nutritional_value[0]}
                else:
                    nutritional_values_calculated[nutritional_value[0]].value = self.__calculate(
                        nutritional_values_calculated[nutritional_value[0]].value, product[2], nutritional_value[2])

        recipe.nutritional_values = nutritional_values_calculated
        self.__database.create(recipe)
