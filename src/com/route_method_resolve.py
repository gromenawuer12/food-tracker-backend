import re

import inject

from .users.infrastructure.api.users_blueprint import resolve as users_resolve
from .weekly_menus.infrastructure.api.weekly_menus_blueprint import resolve as weekly_menu_resolver
from .monthly_menus.infrastructure.api.monthly_menus_blueprint import resolve as monthly_menu_resolver
from .units.infrastructure.api.units_blueprint import resolve as unit_resolver
from .nutritional_values.infrastructure.api.nutritional_value_blueprint import resolve as nutritional_values_resolver
from .products.infrastructure.api.products_blueprint import resolve as products_resolver
from .menus.infrastructure.api.menus_blueprint import resolve as menus_resolver
from .recipes.infrastructure.api.recipes_blueprint import resolve as recipes_resolver
from .utils.log import Log

paths = {
    r"\/users.*": users_resolve,
    r"\/weekly_menus.*": weekly_menu_resolver,
    r"\/monthly_menus/.*": monthly_menu_resolver,
    r"\/units/.*": unit_resolver,
    r"\/nutritional_value.*": nutritional_values_resolver,
    r"\/products.*": products_resolver,
    r"\/menus.*": menus_resolver,
    r"\/recipes.*": recipes_resolver,
}


@inject.autoparams('log')
def resolve(event, log: Log):
    log.trace('Resolving path: "{0}"'.format(event['path']))
    for key in paths:
        if re.search(key, event['path']):
            try:
                return paths[key](event)
            except KeyError as err:
                error = 'Operation {0} not supported for {1}'.format(event['httpMethod'], event['path'])
                log.error(error)
                raise Exception(error)
    log.debug('Path not supported: "{0}"'.format(event['path']))
    raise Exception('Path not supported: "{0}"'.format(event['path']))
