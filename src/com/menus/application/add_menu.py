import inject
from ..domain.menu_database import MenuDatabase
from ...products.application.get_product import GetProduct
from ...recipes.application.add_recipe import AddRecipe
from ...recipes.application.delete_recipe import DeleteRecipe
from ...recipes.application.get_recipe import GetRecipe
from ...utils.log import Log


class AddMenu:
    @inject.autoparams()
    def __init__(self, database: MenuDatabase, get_recipe: GetRecipe, get_product: GetProduct,
                 delete_recipe: DeleteRecipe, add_recipe: AddRecipe, log: Log):
        self.__database = database
        self.__get_recipe = get_recipe
        self.__delete_recipe = delete_recipe
        self.__add_recipe = add_recipe
        self.__get_product = get_product
        self.__log = log

    def execute(self, menu):
        self.__log.trace('AddMenu menu: {0}', menu.to_json())
        nutritional_value_calculated = {}
        parts_of_day = {}

        if isinstance(menu.products, dict):
            self.__parts_of_day(menu, nutritional_value_calculated, parts_of_day)
        else:
            self.__without_parts_of_day(menu, nutritional_value_calculated)

        self.__log.trace("AddMenu nutritional_value={0}", nutritional_value_calculated)

        nutritional_value_calculated_array = []
        for nutritional_value_name in nutritional_value_calculated:
            nutritional_value_calculated_array.append(nutritional_value_calculated[nutritional_value_name])

        self.__log.trace("AddMenu nutritional_value_array={0}", nutritional_value_calculated_array)
        menu.nutritional_value = nutritional_value_calculated_array

        self.__database.create(menu)

    def __parts_of_day(self, menu, nutritional_value_calculated, parts_of_day):
        self.__log.trace("AddMenu __parts_of_day products {0}", menu.products)
        for part_of_day in menu.products:
            products = menu.products[part_of_day]
            self.__log.trace("AddMenu __part_of_day {0} {1}", part_of_day, products)
            for product in products:
                parts_of_day[part_of_day] = product
                nutritional_value = self.__get_product.execute(product['name'])['nutritional_value']
                self.__log.trace('AddMenu product: {0} with {1}', product, nutritional_value)
                quantity = float(product['value'])

                for nutritional_value_element in nutritional_value:
                    self.__log.trace('AddMenu nutritional_value_element: {0}', nutritional_value_element)
                    multiply_by = quantity if 'recipe_name' in product and product['recipe_name'] else quantity / 100
                    value = float(nutritional_value_element[2]) * multiply_by

                    if nutritional_value_element[0] in nutritional_value_calculated:
                        nutritional_value_calculated[nutritional_value_element[0]]['value'] = str(round(
                            float(nutritional_value_calculated[nutritional_value_element[0]]['value']) +
                            value, 2))
                    else:
                        self.__log.trace('AddMenu nutritional_value_element.name: {0}', nutritional_value_element[0])
                        nutritional_value_calculated[nutritional_value_element[0]] = \
                            {
                                'unit': nutritional_value_element[1],
                                'value': str(round(value, 2)),
                                'name': nutritional_value_element[0],
                            }

    def __without_parts_of_day(self, menu, nutritional_value_calculated):
        for recipe_name in menu.recipes:
            recipe = self.__get_recipe.execute(recipe_name)
            self.__log.trace('AddMenu recipe: {0}', recipe)

            for nutritional_value_element in recipe['nutritional_value']:
                self.__log.trace('AddMenu nutritional_value_element: {0}', nutritional_value_element)
                if nutritional_value_element['name'] in nutritional_value_calculated:
                    nutritional_value_calculated[nutritional_value_element['name']]['value'] = str(round(
                        float(nutritional_value_calculated[nutritional_value_element['name']]['value']) +
                        float(nutritional_value_element['value']), 2))
                else:
                    self.__log.trace('AddMenu nutritional_value_element.name: {0}', nutritional_value_element['name'])
                    nutritional_value_calculated[nutritional_value_element['name']] = \
                        {
                            'unit': nutritional_value_element['unit'],
                            'value': nutritional_value_element['value'],
                            'name': nutritional_value_element['name'],
                        }

        for product in menu.products:
            nutritional_value = self.__get_product.execute(product['name'])['nutritional_value']
            self.__log.trace('AddMenu product: {0} with {1}', product, nutritional_value)
            quantity = float(product['value'])

            for nutritional_value_element in nutritional_value:
                self.__log.trace('AddMenu nutritional_value_element: {0}', nutritional_value_element)
                multiply_by = quantity if 'recipe_name' in product and product['recipe_name'] else quantity / 100
                value = float(nutritional_value_element[2]) * multiply_by

                if nutritional_value_element[0] in nutritional_value_calculated:
                    nutritional_value_calculated[nutritional_value_element[0]]['value'] = str(round(
                        float(nutritional_value_calculated[nutritional_value_element[0]]['value']) +
                        value, 2))
                else:
                    self.__log.trace('AddMenu nutritional_value_element.name: {0}', nutritional_value_element[0])
                    nutritional_value_calculated[nutritional_value_element[0]] = \
                        {
                            'unit': nutritional_value_element[1],
                            'value': str(round(value, 2)),
                            'name': nutritional_value_element[0],
                        }
