import json

import inject

from ...application.add_unit import AddUnit
from ...application.delete_unit import DeleteUnit
from ...application.edit_unit import EditUnit
from ...application.get_unit import GetUnit
from ...domain.unit import Unit
from ....resources.token.token_required_decorator import token_required
from ....utils.log import Log


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
    def __init__(self, get_unit: GetUnit, add_unit: AddUnit, edit_unit: EditUnit, delete_unit: DeleteUnit, log: Log):
        self.get_unit = get_unit
        self.add_unit = add_unit
        self.edit_unit = edit_unit
        self.delete_unit = delete_unit
        self.log = log

    @token_required
    def get(self, event):
        self.log.debug('get units')
        return self.get_unit.execute(event['pathParameters'].get('shortname', None))

    @token_required
    def post(self, event):
        body = json.loads(event['body'])
        self.log.debug(body)
        self.add_unit.execute(Unit(body))
        return {}

    @token_required
    def delete(self, event):
        body = json.loads(event['body'])
        shortname = body.get('shortname', None)
        self.delete_unit.execute(shortname)

    @token_required
    def put(self, event):
        self.log.debug('put: proxy={0}', json.dumps(event['pathParameters']['proxy']))
        shortname = event['pathParameters']['proxy'].split('/')[1]
        self.log.trace('put: shortname={0}', shortname)

        if shortname is None:
            raise Exception

        body = json.loads(event['body'])
        self.log.trace('put: body={0}', body)

        self.edit_unit.execute(shortname, Unit(body))

