import base64
import hashlib
from types import SimpleNamespace

import datetime
import inject
import json
import jwt
import os
import requests
from requests import Response
from werkzeug.security import check_password_hash

from .login_exception import LoginException
from ...application.add_user import AddUser
from ...application.get_user import GetUser
from ...application.login_user import LoginUser
from ...application.remove_underscore import remove_underscore
from ...application.update_user import UpdateUser
from ...domain.user import User

# from ....resources.token.token_optional_decorator import token_optional
# from ....resources.token.token_required_decorator import token_required
class UsersBlueprint:
    @inject.autoparams()
    def __init__(self, get_user: GetUser, add_user: AddUser, login_user: LoginUser, update_user: UpdateUser):
        self.__get_user = get_user
        self.__add_user = add_user
        self.__login_user = login_user
        self.__update_user = update_user

    # @inject.autoparams()
    # def create_users_blueprint(get_user: GetUser, add_user: AddUser, login_user: LoginUser, update_user: UpdateUser):
    # users_blueprint = Blueprint('users', __name__)

    # @users_blueprint.route('/<username>',methods=['GET'])
    # @token_optional
    @remove_underscore
    def get(self, auth_username, username) -> Response:
        return self.__get_user.execute(username, auth_username)

    # @users_blueprint.route('/',methods=['POST'])
    def post(self, body) -> Response:
        # return self.__add_user.execute(User(json.loads(json.dumps(body), object_hook=lambda d: SimpleNamespace(**d).__dict__)))
        return body

    # @users_blueprint.route('/login',methods=['POST'])
    def login(self, headers) -> Response:
        auth = base64.b64decode(headers['Authorization'].split(' ')[1]).decode('utf-8')
        if auth is None:
            raise LoginException("Invalid login")
        username = auth.split(':')[0]
        password = auth.split(':')[1]
        user = self.__login_user.execute(username)
        if user is None or not check_password_hash(user['password'], password):
            raise LoginException("Invalid username or password")
        token = jwt.encode(
            {'username': user['username'], 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30), },
            os.getenv('SECRET_KEY'), algorithm="HS256")

        """ 
        menusBlocked = json.loads(requests.get(os.getenv('ENDPOINT_URL') + 'menus/block',
                                               # headers={'Authorization': 'access_token ' + token}).content.decode(
            # "utf-8"))
        if menusBlocked:
            for item in menusBlocked:
                data = {'user': user['username'], 'date': item['date'], 'nutritional_value': item['nutritional_value']}
                requests.post(os.getenv('ENDPOINT_URL') + 'weekly_menus/',
                              headers={'Authorization': 'access_token ' + token}, json=data)
                requests.post(os.getenv('ENDPOINT_URL') + 'monthly_menus/',
                              headers={'Authorization': 'access_token ' + token}, json=data)
        """
        return {"token": token, "user": user['username']}

    # @users_blueprint.route('/<username>',methods=['PUT'])
    # @token_required
    def modify(self, auth_username, username) -> Response:
        if auth_username != username:
            raise Exception
        user = self.__login_user.execute(username)
        new_password = requests.get("new_password") if requests.get("new_password") else user[
            '_password']
        new_role = requests.get("new_role") if requests.get("new_role") else user['role']

        self.__update_user.execute(user['username'], new_password, new_role)
        return {}

    # return users_blueprint
