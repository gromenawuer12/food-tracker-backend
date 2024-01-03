import base64
import datetime
import os
import re

import inject
import jwt

from ...application.get_user import GetUser
from ....utils.log import Log
from ...application.login_user import LoginUser
from ...infrastructure.api.login_exception import LoginException


def resolve(event):
    users_blueprint = UsersBlueprint()
    if re.search('/users/login', event['path']):
        return users_blueprint.login(event['headers'])
    return {
        "GET": users_blueprint.get,
    }[event['httpMethod']](event=event)


class UsersBlueprint:
    @inject.autoparams()
    def __init__(self, login_user: LoginUser, get_user: GetUser, log: Log):
        log.debug('init - UsersBlueprint')
        self.login_user = login_user
        self.get_user = get_user
        self.log = log

    def get(self, event):
        self.log.debug('UsersBlueprint - get')
        return self.get_user.execute()

    def login(self, headers):
        self.log.debug('UsersBlueprint: login')
        auth = base64.b64decode(headers['Authorization'].split(' ')[1]).decode('utf-8')

        if auth is None:
            raise LoginException("Invalid login")

        username = auth.split(':')[0]
        password = auth.split(':')[1]
        user = self.login_user.execute(username, password)
        self.log.trace('UsersBlueprint login: user logged')

        token = jwt.encode({
            'username': user['username'],
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30), },
            os.getenv('SECRET_KEY'),
            algorithm="HS256"
        )
        self.log.trace('UsersBlueprint login: Token generated')

        return {"token": token, "user": user['username']}
