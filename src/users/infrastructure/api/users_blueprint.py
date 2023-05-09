import base64
import hashlib
from types import SimpleNamespace

import datetime
import inject
import json
import jwt
import os
import re
from requests import Response
from werkzeug.security import check_password_hash

from .login_exception import LoginException
from ...application.add_user import AddUser
from ...application.get_user import GetUser
from ...application.login_user import LoginUser
from ...application.remove_underscore import remove_underscore
from ...application.update_user import UpdateUser
from ...domain.user import User

from ....resources.token.token_optional_decorator import token_optional
from ....resources.token.token_required_decorator import token_required

from ....menus.infrastructure.api.menus_blueprint import MenusBlueprint
from ....monthly_menus.infrastructure.api.monthly_menus_blueprint import MonthlyMenusBlueprint
from ....weekly_menus.infrastructure.api.weekly_menus_blueprint import WeeklyMenusBlueprint

def resolve(event):
    usersBlueprint = UsersBlueprint()
    if re.search('/users/login', event['path']):
        return usersBlueprint.login(event['headers'])
    return eval({
                    "GET": "usersBlueprint.get(pathParameters=event['pathParameters'], headers=event['headers'])",
                    "POST": "usersBlueprint.post(event['body'])",
                    "PUT": "usersBlueprint.modify(headers=event['headers'],pathParameters=event['pathParameters'], body=event['body'])"
                }[event['httpMethod']])

class UsersBlueprint:
    @inject.autoparams()
    def __init__(self, get_user: GetUser, add_user: AddUser, login_user: LoginUser, update_user: UpdateUser):
        self.get_user = get_user
        self.add_user = add_user
        self.login_user = login_user
        self.update_user = update_user

    @token_required
    # @remove_underscore
    def get(self, auth_username, headers) -> Response:
        print("GET USER")
        return self.get_user.execute()

    def post(self, body) -> Response:
        return self.add_user.execute(User(json.loads(body, object_hook=lambda d: SimpleNamespace(**d).__dict__)))

    def login(self, headers) -> Response:
        auth = base64.b64decode(headers['Authorization'].split(' ')[1]).decode('utf-8')
        if auth is None:
            raise LoginException("Invalid login")
        username = auth.split(':')[0]
        password = auth.split(':')[1]
        user = self.login_user.execute(username)
        if user is None or not check_password_hash(user['password'], password):
            raise LoginException("Invalid username or password")
        token = jwt.encode(
            {'username': user['username'], 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30), },
            os.getenv('SECRET_KEY'), algorithm="HS256")
        headers["Authorization"] = "Bearer "+token
        menusBlueprint = MenusBlueprint()
        weeklyMenusBlueprint = WeeklyMenusBlueprint()
        monthlyMenusBlueprint = MonthlyMenusBlueprint()
        menusBlocked = json.loads(menusBlueprint.block(headers=headers))
        if menusBlocked:
            for item in menusBlocked:
                data = {'user': user['username'], 'date': item['date'], 'nutritional_value': item['nutritional_value']}
            weeklyMenusBlueprint.post(headers=headers, body=json.dumps(data))
            monthlyMenusBlueprint.post(headers=headers, body=json.dumps(data))

        return {"token": token, "user": user['username']}

    @token_required
    def modify(self, auth_username, pathParameters, headers, body) -> Response:
        username = pathParameters.get('username', None)
        if auth_username != username:
            raise Exception
        user = self.login_user.execute(username)
        body = json.loads(body)
        new_password = body.get("new_password", user["password"])
        new_role = body.get("new_role", user["role"])

        self.update_user.execute(user["username"], new_password, new_role)
        return {}
