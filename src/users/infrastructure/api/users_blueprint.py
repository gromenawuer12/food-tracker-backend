from werkzeug.security import check_password_hash
import inject, json, jwt, datetime, os, sys, requests
from types import SimpleNamespace
from flask import Blueprint, Response, request
from users.application.login_user import LoginUser
from .login_exception import LoginException
from ...application.add_user import AddUser
from ...application.get_user import GetUser
from ...application.update_user import UpdateUser
from menus.application.block_menu import BlockMenu
from ...domain.user import User
from resources.token.token_optional_decorator import token_optional
from resources.token.token_required_decorator import token_required
from ...application.remove_underscore import remove_underscore
from datetime import date


@inject.autoparams()
def create_users_blueprint(get_user: GetUser, add_user: AddUser,login_user: LoginUser, update_user: UpdateUser, block_menu: BlockMenu) -> Blueprint:
    users_blueprint = Blueprint('users', __name__)

    @users_blueprint.route('/<username>',methods=['GET'])
    @token_optional
    @remove_underscore
    def get(auth_username,username) -> Response:
        return get_user.execute(username, auth_username)

    @users_blueprint.route('/',methods=['POST'])
    def post() -> Response:
        return add_user.execute(User(json.loads(json.dumps(request.get_json()),object_hook=lambda d: SimpleNamespace(**d).__dict__)))

    @users_blueprint.route('/login',methods=['POST'])
    def login() -> Response:
        auth = request.authorization
        if auth is None:
            raise LoginException("Invalid login")
        user = login_user.execute(auth.get('username'))
        if user is None or not check_password_hash(user['password'],auth.password):
            raise LoginException("Invalid username or password")
        # modify to work local and remote
        token = jwt.encode({'username': user['username'], 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30),}, os.getenv('SECRET_KEY'),algorithm="HS256")
        menusBlocked = json.loads(requests.get(os.getenv('ENDPOINT_URL')+'menus/block',headers={'Authorization': 'access_token '+token}).content.decode("utf-8"))
        if menusBlocked:
            for item in menusBlocked:
                data = {'user':user['username'],'date':item['date'],'nutritional_value':item['nutritional_value']}
                requests.post(os.getenv('ENDPOINT_URL')+'weekly_menus/',headers={'Authorization':'access_token '+token},json=data)
                requests.post(os.getenv('ENDPOINT_URL')+'monthly_menus/',headers={'Authorization':'access_token '+token},json=data)
        return {"token":token, "user": user['username']}

    @users_blueprint.route('/<username>',methods=['PUT'])
    @token_required
    def modify(auth_username, username) -> Response:    
        if auth_username!=username:
            raise Exception
        user = login_user.execute(username)
        new_password = request.get_json().get("new_password") if request.get_json().get("new_password") else user['_password']
        new_role = request.get_json().get("new_role") if request.get_json().get("new_role") else user['role']

        update_user.execute(user['username'], new_password, new_role)
        return "Updated"

    return users_blueprint