from flask import Flask
import inject, boto3, os
from users.domain.user_database import UserDatabase
from units.domain.unit_database import UnitDatabase
from products.domain.product_database import ProductDatabase
from recipes.domain.recipe_database import RecipeDatabase
from menus.domain.menu_database import MenuDatabase
from monthly_menus.domain.monthly_menu_database import MonthlyMenuDatabase
from weekly_menus.domain.weekly_menu_database import WeeklyMenuDatabase
from nutritional_value.domain.nutritional_value_database import NutritionalValueDatabase
from users.infrastructure.database.user_dynamodb import UserDynamoDB
from units.infrastructure.database.unit_dynamodb import UnitDynamoDB
from products.infrastructure.database.product_dynamodb import ProductDynamoDB
from recipes.infrastructure.database.recipe_dynamodb import RecipeDynamoDB
from menus.infrastructure.database.menu_dynamodb import MenuDynamoDB
from weekly_menus.infrastructure.database.weekly_menu_dynamodb import WeeklyMenuDynamoDB
from monthly_menus.infrastructure.database.monthly_menu_dynamodb import MonthlyMenuDynamoDB
from nutritional_value.infrastructure.database.nutritional_value_dynamodb import NutritionalValueDynamoDB

client = boto3.resource('dynamodb', region_name=os.getenv('REGION_NAME'), endpoint_url=os.getenv('ENDPOINT_URL'), aws_access_key_id=os.getenv('ACCESS_KEY_ID'), aws_secret_access_key=os.getenv('SECRET_ACCESS_KEY'))

def configure_inject(app: Flask) -> None:
    def config(binder: inject.Binder) -> None:
        binder.bind(UserDatabase, UserDynamoDB(client))
        binder.bind(UnitDatabase, UnitDynamoDB(client))
        binder.bind(ProductDatabase, ProductDynamoDB(client))
        binder.bind(RecipeDatabase, RecipeDynamoDB(client))
        binder.bind(MenuDatabase, MenuDynamoDB(client))
        binder.bind(MonthlyMenuDatabase, MonthlyMenuDynamoDB(client))
        binder.bind(WeeklyMenuDatabase, WeeklyMenuDynamoDB(client))
        binder.bind(NutritionalValueDatabase, NutritionalValueDynamoDB(client))

    inject.configure(config)