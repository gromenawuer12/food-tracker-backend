import inject, boto3, os

from .menus.domain.menu_database import MenuDatabase
from .menus.infrastructure.database.menu_dynamodb import MenuDynamoDB
from .monthly_menus.domain.monthly_menu_database import MonthlyMenuDatabase
from .monthly_menus.infrastructure.database.monthly_menu_dynamodb import MonthlyMenuDynamoDB
from .nutritional_values.domain.nutritional_value_database import NutritionalValueDatabase
from .nutritional_values.infrastructure.database.nutritional_value_dynamodb import NutritionalValueDynamoDB
from .products.domain.product_database import ProductDatabase
from .products.infrastructure.database.product_dynamodb import ProductDynamoDB
from .recipes.domain.recipe_database import RecipeDatabase
from .settings.domain.settings_database import SettingsDatabase
from .settings.infrastructure.database.settings_dynamodb import SettingsDynamoDB
from .units.domain.unit_database import UnitDatabase
from .units.infrastructure.database.unit_dynamodb import UnitDynamoDB
from .users.domain.user_database import UserDatabase
from .users.infrastructure.database.user_dynamodb import UserDynamoDB
from .utils.log import Log
from .weekly_menus.domain.weekly_menu_database import WeeklyMenuDatabase
from .weekly_menus.infrastructure.database.weekly_menu_dynamodb import WeeklyMenuDynamoDB
from .recipes.infrastructure.database.recipe_dynamodb import RecipeDynamoDB


def configure_inject(request_id) -> None:
    client = boto3.resource('dynamodb', region_name=os.getenv('REGION_NAME'), endpoint_url=os.getenv('DB_URL'),
                            aws_access_key_id=os.getenv('ACCESS_KEY_ID'),
                            aws_secret_access_key=os.getenv('SECRET_ACCESS_KEY'))

    def config(binder: inject.Binder) -> None:
        print(request_id + ' -> configure_inject')
        log = Log(request_id)
        binder.bind(Log, log)
        binder.bind(UserDatabase, UserDynamoDB(client, log))
        binder.bind(WeeklyMenuDatabase, WeeklyMenuDynamoDB(client))
        binder.bind(MonthlyMenuDatabase, MonthlyMenuDynamoDB(client))
        binder.bind(UnitDatabase, UnitDynamoDB(client))
        binder.bind(NutritionalValueDatabase, NutritionalValueDynamoDB(client, log))
        binder.bind(ProductDatabase, ProductDynamoDB(client, log))
        binder.bind(MenuDatabase, MenuDynamoDB(client, log))
        binder.bind(RecipeDatabase, RecipeDynamoDB(client, log))
        binder.bind(SettingsDatabase, SettingsDynamoDB(client, log))

    if not inject.is_configured():
        inject.configure(config)
