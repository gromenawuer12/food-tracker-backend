import inject
import json

from ...application.add_menu import AddMenu
from ...application.block_menu import BlockMenu
from ...application.delete_menu import DeleteMenu
from ...application.edit_menu import EditMenu
from ...application.get_menu import GetMenu
from ...domain.menu import Menu
from ....resources.token.token_required_decorator import token_required
from ....utils.log import Log


def resolve(event):
    menus_blueprint = MenusBlueprint()
    return {'GET': menus_blueprint.get,
            'POST': menus_blueprint.post,
            'PUT': menus_blueprint.put,
            'DELETE': menus_blueprint.delete
            }[event['httpMethod']](event=event)


class MenusBlueprint:
    @inject.autoparams()
    def __init__(self, get_menu: GetMenu, add_menu: AddMenu, edit_menu: EditMenu, delete_menu: DeleteMenu,
                 block_menu: BlockMenu, log: Log):
        self.get_menu = get_menu
        self.add_menu = add_menu
        self.delete_menu = delete_menu
        self.block_menu = block_menu
        self.edit_menu = edit_menu
        self.log = log

    @token_required
    def get(self, event):
        self.log.debug('MenusBlueprint get: queryStringParameters={0}', event['queryStringParameters'])
        query_string_parameters = event['queryStringParameters']
        return self.get_menu.execute(query_string_parameters)

    @token_required
    def post(self, event):
        self.log.trace('MenusBlueprint post')
        menu = Menu(json.loads(event['body']))
        self.add_menu.execute(menu)

    @token_required
    def put(self, event):
        self.log.debug('MenusBlueprint put: proxy={0}', json.dumps(event['pathParameters']['proxy']))
        path_id = event['pathParameters']['proxy'].split('/')[1]
        self.log.trace('MenusBlueprint put: shortname={0}', path_id)

        if path_id is None:
            raise Exception

        body = json.loads(event['body'])
        self.log.trace('MenusBlueprint put: body={0}', body)

        self.edit_menu.execute(path_id, Menu(body))

    @token_required
    def delete(self, event):
        body = json.loads(event['body'])
        self.log.debug('MenusBlueprint delete: {0}', body)

        attrs = body['id'].split('|')
        username = attrs[0]
        date = attrs[1]

        self.log.debug('MenusBlueprint delete: date={0} and username={1}', date, username)

        self.delete_menu.execute(username, date)
