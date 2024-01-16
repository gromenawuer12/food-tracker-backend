import inject
from ..domain.recipe import Recipe
from ..domain.recipe_database import RecipeDatabase
from ...products.application.get_product import GetProduct
from ...utils.log import Log


def calculate(other, value, grams):
    return str(round(float(other) + (float(value) * float(grams) / 100), 2))


class AddRecipe:
    @inject.autoparams()
    def __init__(self, database: RecipeDatabase, get_product: GetProduct, log: Log):
        self.__database = database
        self.__get_product = get_product
        self.__log = log

    def execute(self, recipe: Recipe):
        self.__log.trace("AddRecipe: {0}", recipe.to_json())
        nutritional_value_calculated = {}
        products = recipe.products
        for product in products:
            self.__log.trace("->AddRecipe calculating for product: {0}", product)
            obj_product = self.__get_product.execute(product[0]);
            self.__log.trace("->AddRecipe product found {0}", obj_product)
            nutritional_value = obj_product['nutritional_value']
            self.__log.trace("->AddRecipe nutritional_value: {0}", nutritional_value)
            for nutritional_value_component in nutritional_value:
                self.__log.trace("-->AddRecipe nutritional_value_component: {0}", nutritional_value_component)
                if nutritional_value_component[0] not in nutritional_value_calculated:
                    self.__log.trace("--->AddRecipe nutritional_value_component not calculated")
                    nutritional_value_calculated[nutritional_value_component[0]] = \
                        {
                            'unit': nutritional_value_component[1],
                            'value': calculate(0, product[2], nutritional_value_component[2]),
                            'name': nutritional_value_component[0]
                        }
                else:
                    self.__log.trace("--->AddRecipe nutritional_value_component was calculated")
                    nutritional_value_calculated[nutritional_value_component[0]]['value'] = calculate(
                        nutritional_value_calculated[nutritional_value_component[0]]['value'], product[2],
                        nutritional_value_component[2])

        self.__log.trace("AddRecipe nutritional_value={0}", nutritional_value_calculated)
        nutritional_value_calculated_array = []
        for nutritional_value_name in nutritional_value_calculated:
            nutritional_value_calculated_array.append(nutritional_value_calculated[nutritional_value_name])

        self.__log.trace("AddRecipe nutritional_value_array={0}", nutritional_value_calculated_array)

        recipe.nutritional_value = nutritional_value_calculated_array
        self.__database.create(recipe)
