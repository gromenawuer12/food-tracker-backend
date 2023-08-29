from types import SimpleNamespace
import inject, json
from requests import Response
from ...application.add_nutritional_value import AddNutritionalValue
from ...application.get_nutritional_value import GetNutritionalValue
from ...application.delete_nutritional_value import DeleteNutritionalValue
from ...domain.nutritional_value import NutritionalValue
from ....resources.token.token_required_decorator import token_required


def resolve(event):
    nutritonal_values_blueprint = NutritionalValueBlueprint()
    return {
        "GET": nutritonal_values_blueprint.get,
        "POST": nutritonal_values_blueprint.post,
        "DELETE": nutritonal_values_blueprint.delete
    }[event['httpMethod']](event=event)


class NutritionalValueBlueprint:
    @inject.autoparams()
    def __init__(self, get_nutritional_value: GetNutritionalValue, add_nutritional_value: AddNutritionalValue,
                 delete_nutritional_value: DeleteNutritionalValue):
        self.get_nutritional_value = get_nutritional_value
        self.add_nutritional_value = add_nutritional_value
        self.delete_nutritional_value = delete_nutritional_value

    @token_required
    def get(self, event) -> Response:
        shortname = event['pathParameters'].get("shortname", None)
        return self.get_nutritional_value.execute(shortname)

    @token_required
    def post(self, event) -> Response:
        return self.add_nutritional_value.execute(
            NutritionalValue(json.loads(event['body'], object_hook=lambda d: SimpleNamespace(**d).__dict__)))

    @token_required
    def delete(self, event) -> Response:
        body = json.loads(event['body'])
        shortname = body.get('shortname', None)
        return self.delete_nutritional_value.execute(shortname)

    @token_required
    def modify(self, event) -> Response:
        shortname = event['pathParameters'].get('shortname', None)
        if shortname is None:
            raise Exception
        nutritional_value = self.get_nutritional_value.execute(shortname)
        body = json.loads(event['body'])
        new_shortname = body.get("new_shortname", nutritional_value["shortname"])
        new_name = body.get("new_name", nutritional_value["name"])
        new_unit = body.get("new_unit", nutritional_value["unit"])

        self.delete_nutritional_value.execute(shortname)
        self.add_nutritional_value.execute(NutritionalValue(
            json.loads({"shortname": new_shortname, "name": new_name, "unit": new_unit},
                       object_hook=lambda d: SimpleNamespace(**d).__dict__)))
        return {}
