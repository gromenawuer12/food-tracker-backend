from types import SimpleNamespace
import inject, json
from requests import Response
from ...application.add_unit import AddUnit
from ...application.get_unit import GetUnit
from ...application.delete_unit import DeleteUnit
from ...domain.unit import Unit
from ....resources.token.token_required_decorator import token_required


def resolve(event):
    unitsBlueprint = UnitsBlueprint()
    return eval({
                    "GET": "unitsBlueprint.get(headers=event['headers'], queryStringParameters=event['queryStringParameters'])",
                    "POST": "unitsBlueprint.post(headers=event['headers'], body=event['body'])",
                    "DELETE": "unitsBlueprint.delete(headers=event['headers'], body=event['body'])"
                }[event['httpMethod']])


class UnitsBlueprint:
    @inject.autoparams()
    def __init__(self, get_unit: GetUnit, add_unit: AddUnit, delete_unit: DeleteUnit):
        self.get_unit = get_unit
        self.add_unit = add_unit
        self.delete_unit = delete_unit

    # @units_blueprint.route('/',methods=['GET'], defaults={'shortname': None})
    # @units_blueprint.route('/<shortname>',methods=['GET'])
    @token_required
    def get(self, auth_username, queryStringParameters, headers) -> Response:
        shortname = queryStringParameters.get('shortname', None)
        return json.dumps(self.get_unit.execute(shortname))

    # @units_blueprint.route('/',methods=['POST'])
    @token_required
    def post(self, auth_username, body, headers) -> Response:
        return self.add_unit.execute(Unit(json.loads(body, object_hook=lambda d: SimpleNamespace(**d).__dict__)))

    #  @units_blueprint.route('/',methods=['DELETE'])
    @token_required
    def delete(self, auth_username, body, headers) -> Response:
        body = json.loads(body)
        shortname = body.get('shortname', None)
        return self.delete_unit.execute(shortname)

    @token_required
    def modify(self, auth_username, queryStringParameters, headers, body) -> Response:
        shortname = queryStringParameters.get('shortname', None)
        if shortname is None:
            raise Exception
        unit = self.get_unit.execute(shortname)
        body = json.loads(body)
        new_shortname = body.get("new_shortname", unit["shortname"])
        new_name = body.get("new_name", unit["name"])

        self.delete_unit.execute(shortname)
        self.add_unit.execute(Unit(json.loads('{"shortname": new_shortname, "name": new_name}', object_hook=lambda d: SimpleNamespace(**d).__dict__)))
        return {}
