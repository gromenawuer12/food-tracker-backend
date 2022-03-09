from flask_lambda import FlaskLambda
from users.domain.user_exception import UserException
from units.domain.unit_exception import UnitException
from products.domain.product_exception import ProductException
from recipes.domain.recipe_exception import RecipeException
from menus.domain.menu_exception import MenuException
from weekly_menus.domain.weekly_menu_exception import WeeklyMenuException
from monthly_menus.domain.monthly_menu_exception import MonthlyMenuException
from nutritional_value.domain.nutritional_value_exception import NutritionalValueException
from exception_handler import handle_exception
from users.infrastructure.api.users_blueprint import create_users_blueprint
from units.infrastructure.api.units_blueprint import create_units_blueprint
from products.infrastructure.api.products_blueprint import create_products_blueprint
from recipes.infrastructure.api.recipes_blueprint import create_recipes_blueprint
from menus.infrastructure.api.menus_blueprint import create_menus_blueprint
from monthly_menus.infrastructure.api.monthly_menus_blueprint import create_monthly_menus_blueprint
from weekly_menus.infrastructure.api.weekly_menus_blueprint import create_weekly_menus_blueprint
from nutritional_value.infrastructure.api.nutritional_value_blueprint import create_nutritional_value_blueprint
from config import configure_inject
from flask_cors import CORS

app = FlaskLambda(__name__)
CORS(app)
configure_inject(app)

app.register_error_handler(UserException,handle_exception)
app.register_error_handler(UnitException,handle_exception)
app.register_error_handler(ProductException,handle_exception)
app.register_error_handler(RecipeException,handle_exception)
app.register_error_handler(NutritionalValueException,handle_exception)
app.register_error_handler(MenuException,handle_exception)
app.register_error_handler(MonthlyMenuException,handle_exception)
app.register_error_handler(WeeklyMenuException,handle_exception)

app.register_blueprint(create_users_blueprint(), url_prefix='/users')
app.register_blueprint(create_units_blueprint(), url_prefix='/units')
app.register_blueprint(create_nutritional_value_blueprint(), url_prefix='/nutritional_value')
app.register_blueprint(create_products_blueprint(), url_prefix='/products')
app.register_blueprint(create_recipes_blueprint(), url_prefix='/recipes')
app.register_blueprint(create_menus_blueprint(), url_prefix='/menus')
app.register_blueprint(create_monthly_menus_blueprint(), url_prefix='/monthly_menus')
app.register_blueprint(create_weekly_menus_blueprint(), url_prefix='/weekly_menus')
    