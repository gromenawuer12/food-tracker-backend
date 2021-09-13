from flask_lambda import FlaskLambda
from users.domain.user_exception import UserException
from units.domain.unit_exception import UnitException
from exception_handler import handle_exception
from users.infrastructure.api.users_blueprint import create_users_blueprint
from units.infrastructure.api.units_blueprint import create_units_blueprint
from config import configure_inject
from flask_cors import CORS

app = FlaskLambda(__name__)
CORS(app)
configure_inject(app)

app.register_error_handler(UserException,handle_exception)
app.register_error_handler(UnitException,handle_exception)

app.register_blueprint(create_users_blueprint(), url_prefix='/users')
app.register_blueprint(create_units_blueprint(), url_prefix='/units')
    