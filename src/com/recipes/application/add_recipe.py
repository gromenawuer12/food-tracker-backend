import inject
from ..domain.recipe import Recipe
from ..domain.recipe_database import RecipeDatabase
from ...products.application.get_product import GetProduct
from ...utils.log import Log


def calculate(other, value):
    return str(round(float(other) + value, 2))


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
            quantity = float(product[2])

            for nutritional_value_component in nutritional_value:
                self.__log.trace("-->AddRecipe nutritional_value_component: {0}", nutritional_value_component)
                multiply_by = quantity if 'portions' in product else quantity / 100
                value = float(nutritional_value_component[2]) * multiply_by

                if nutritional_value_component[0] not in nutritional_value_calculated:
                    self.__log.trace("--->AddRecipe nutritional_value_component not calculated")
                    nutritional_value_calculated[nutritional_value_component[0]] = \
                        {
                            'unit': nutritional_value_component[1],
                            'value': calculate(0, value),
                            'name': nutritional_value_component[0]
                        }
                else:
                    self.__log.trace("--->AddRecipe nutritional_value_component was calculated")
                    nutritional_value_calculated[nutritional_value_component[0]]['value'] = calculate(
                        nutritional_value_calculated[nutritional_value_component[0]]['value'], value)

        self.__log.trace("AddRecipe nutritional_value={0}", nutritional_value_calculated)
        nutritional_value_calculated_array = []
        for nutritional_value_name in nutritional_value_calculated:
            nutritional_value_calculated_array.append(nutritional_value_calculated[nutritional_value_name])

        self.__log.trace("AddRecipe nutritional_value_array={0}", nutritional_value_calculated_array)

        recipe.nutritional_value = nutritional_value_calculated_array
        self.__database.create(recipe)
