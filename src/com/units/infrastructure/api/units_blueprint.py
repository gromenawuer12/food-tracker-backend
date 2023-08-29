import json
from types import SimpleNamespace

import inject

from ...application.add_unit import AddUnit
from ...application.delete_unit import DeleteUnit
from ...application.get_unit import GetUnit
from ...domain.unit import Unit
from ....resources.token.token_required_decorator import token_required


def resolve(event):
    units_blueprint = UnitsBlueprint()
    return {
        "GET": units_blueprint.get,
        "POST": units_blueprint.post,
        "PUT": units_blueprint.put,
        "DELETE": units_blueprint.delete
    }[event['httpMethod']](event=event)


class UnitsBlueprint:
    @inject.autoparams()
    def __init__(self, get_unit: GetUnit, add_unit: AddUnit, delete_unit: DeleteUnit):
        self.get_unit = get_unit
        self.add_unit = add_unit
        self.delete_unit = delete_unit

    @token_required
    def get(self, event):
        return self.get_unit.execute(event['pathParameters'].get('shortname', None))

    @token_required
    def post(self, event):
        self.add_unit.execute(Unit(json.loads(event['body'], object_hook=lambda d: SimpleNamespace(**d).__dict__)))
        return {}

    @token_required
    def delete(self, event):
        body = json.loads(event['body'])
        shortname = body.get('shortname', None)
        self.delete_unit.execute(shortname)
        return {}

    @token_required
    def put(self, event):
        shortname = event['pathParameters'].get('shortname', None)
        if shortname is None:
            raise Exception
        unit = self.get_unit.execute(shortname)
        body = json.loads(event['body'])
        new_shortname = body.get("new_shortname", unit["shortname"])
        new_name = body.get("new_name", unit["name"])

        self.delete_unit.execute(shortname)
        self.add_unit.execute(Unit(json.loads('{"shortname": new_shortname, "name": new_name}',
                                              object_hook=lambda d: SimpleNamespace(**d).__dict__)))
        return {}
