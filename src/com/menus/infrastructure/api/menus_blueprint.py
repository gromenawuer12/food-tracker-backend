from types import SimpleNamespace
import inject, json
from ...application.add_menu import AddMenu
from ...application.get_menu import GetMenu
from ...application.delete_menu import DeleteMenu
from ...application.block_menu import BlockMenu
from ....resources.token.token_required_decorator import token_required
from datetime import date
from ....utils.log import Log


def resolve(event):
    menus_blueprint = MenusBlueprint()
    return {"GET": menus_blueprint.get,
            "POST": menus_blueprint.post,
            "DELETE": menus_blueprint.delete
            }[event['httpMethod']](event=event)


class MenusBlueprint:
    @inject.autoparams()
    def __init__(self, get_menu: GetMenu, add_menu: AddMenu, delete_menu: DeleteMenu, block_menu: BlockMenu, log: Log):
        self.get_menu = get_menu
        self.add_menu = add_menu
        self.delete_menu = delete_menu
        self.block_menu = block_menu
        self.log = log

    @token_required
    def get(self, event):
        user = event['queryStringParameters'].get('user', None)
        fromDate = event['queryStringParameters'].get('from', None)
        toDate = event['queryStringParameters'].get('to', None)

        return self.get_menu.execute(user, fromDate, toDate)

    @token_required
    def post(self, event):
        self.log.trace('MenusBlueprint post')
        body = json.loads(event['body'])
        self.add_menu.execute(body['user'], body['date'], body.get("recipes"))
        return {}

    @token_required
    def delete(self, event):
        body = json.loads(event['body'])
        user = body.get("user", event['auth_username'])
        self.delete_menu.execute(user, body.get("date"))
        return {}
