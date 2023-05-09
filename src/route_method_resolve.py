import re, json

from .units.infrastructure.api.units_blueprint import resolve as units_resolve
from .users.infrastructure.api.users_blueprint import resolve as users_resolve
from .monthly_menus.infrastructure.api.monthly_menus_blueprint import resolve as monthly_menus_resolve
from .weekly_menus.infrastructure.api.weekly_menus_blueprint import resolve as weekly_menus_resolve
from .menus.infrastructure.api.menus_blueprint import resolve as menus_resolve
from .recipes.infrastructure.api.recipes_blueprint import resolve as recipes_resolve
from .nutritional_value.infrastructure.api.nutritional_value_blueprint import resolve as nutritional_values_resolve
from .products.infrastructure.api.products_blueprint import resolve as products_resolve

paths = {
    r"\/users.*": "users_resolve",
    r"\/units.*": "units_resolve",
    r"\/products.*": "products_resolve",
    r"\/recipes.*": "recipes_resolve",
    r"\/menus.*": "menus_resolve",
    r"\/monthly_menus.*": "monthly_menus_resolve",
    r"\/weekly_menus.*": "weekly_menus_resolve",
    r"\/nutritional_value.*": "nutritional_values_resolve",
}


def resolve(event):
    for key in paths:
        if re.search(key, event['path']):
            return eval(paths[key])(event)
