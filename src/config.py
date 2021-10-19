from flask import Flask
import inject
from users.domain.user_database import UserDatabase
from units.domain.unit_database import UnitDatabase
from products.domain.product_database import ProductDatabase
from recipes.domain.recipe_database import RecipeDatabase
from nutritional_value.domain.nutritional_value_database import NutritionalValueDatabase
from users.infrastructure.database.user_dynamodb import UserDynamoDB
from units.infrastructure.database.unit_dynamodb import UnitDynamoDB
from products.infrastructure.database.product_dynamodb import ProductDynamoDB
from recipes.infrastructure.database.recipe_dynamodb import RecipeDynamoDB
from nutritional_value.infrastructure.database.nutritional_value_dynamodb import NutritionalValueDynamoDB

def configure_inject(app: Flask) -> None:
    def config(binder: inject.Binder) -> None:
        binder.bind(UserDatabase, UserDynamoDB())
        binder.bind(UnitDatabase, UnitDynamoDB())
        binder.bind(ProductDatabase, ProductDynamoDB())
        binder.bind(RecipeDatabase, RecipeDynamoDB())
        binder.bind(NutritionalValueDatabase, NutritionalValueDynamoDB())

    inject.configure(config)