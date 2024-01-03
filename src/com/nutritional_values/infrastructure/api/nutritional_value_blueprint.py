import inject
import json

from ...application.add_nutritional_value import AddNutritionalValue
from ...application.delete_nutritional_value import DeleteNutritionalValue
from ...application.edit_nutritional_value import EditNutritionalValue
from ...application.get_nutritional_value import GetNutritionalValue
from ...domain.nutritional_value import NutritionalValue
from ....resources.token.token_required_decorator import token_required
from ....utils.log import Log


def resolve(event):
    nutritonal_values_blueprint = NutritionalValueBlueprint()
    return {
        "GET": nutritonal_values_blueprint.get,
        "POST": nutritonal_values_blueprint.post,
        "PUT": nutritonal_values_blueprint.put,
        "DELETE": nutritonal_values_blueprint.delete
    }[event['httpMethod']](event=event)


class NutritionalValueBlueprint:
    @inject.autoparams()
    def __init__(self, get_nutritional_value: GetNutritionalValue, add_nutritional_value: AddNutritionalValue,
                 edit_nutritional_value: EditNutritionalValue, delete_nutritional_value: DeleteNutritionalValue, log: Log):
        self.get_nutritional_value = get_nutritional_value
        self.add_nutritional_value = add_nutritional_value
        self.edit_nutritional_value = edit_nutritional_value
        self.delete_nutritional_value = delete_nutritional_value
        self.log = log

    @token_required
    def get(self, event):
        self.log.debug('NutritionalValueBlueprint get:')
        shortname = event['pathParameters'].get("shortname", None)
        return self.get_nutritional_value.execute(shortname)

    @token_required
    def post(self, event):
        self.log.debug('NutritionalValueBlueprint post:')
        body = json.loads(event['body'])
        self.log.debug(body)
        self.add_nutritional_value.execute(NutritionalValue(body))

    @token_required
    def delete(self, event):
        self.log.debug('NutritionalValueBlueprint delete:')
        body = json.loads(event['body'])
        shortname = body.get('shortname', None)
        return self.delete_nutritional_value.execute(shortname)

    @token_required
    def put(self, event):
        self.log.debug('NutritionalValueBlueprint put: proxy={0}', json.dumps(event['pathParameters']['proxy']))
        shortname = event['pathParameters']['proxy'].split('/')[1]
        self.log.trace('NutritionalValueBlueprint put: shortname={0}', shortname)

        if shortname is None:
            raise Exception

        body = json.loads(event['body'])
        self.log.trace('NutritionalValueBlueprint put: body={0}', body)

        self.edit_nutritional_value.execute(shortname, NutritionalValue(body))
