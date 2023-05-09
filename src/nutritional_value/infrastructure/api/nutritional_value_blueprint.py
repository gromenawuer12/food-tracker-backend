from types import SimpleNamespace
import inject, json
from requests import Response
from ...application.add_nutritional_value import AddNutritionalValue
from ...application.get_nutritional_value import GetNutritionalValue
from ...application.delete_nutritional_value import DeleteNutritionalValue
from ...domain.nutritional_value import NutritionalValue
from ....resources.token.token_required_decorator import token_required


def resolve(event):
    nutritonalValuesBlueprint = NutritionalValueBlueprint()
    return eval({
                    "GET": "nutritonalValuesBlueprint.get(headers=event['headers'], queryStringParameters=event['queryStringParameters'])",
                    "POST": "nutritonalValuesBlueprint.post(headers=event['headers'], body=event['body'])",
                    "DELETE": "nutritonalValuesBlueprint.delete(headers=event['headers'], body=event['body'])"
                }[event['httpMethod']])


class NutritionalValueBlueprint:
    @inject.autoparams()
    def __init__(self, get_nutritional_value: GetNutritionalValue, add_nutritional_value: AddNutritionalValue,
                 delete_nutritional_value: DeleteNutritionalValue):
        self.get_nutritional_value = get_nutritional_value
        self.add_nutritional_value = add_nutritional_value
        self.delete_nutritional_value = delete_nutritional_value

    # @nutritional_value_blueprint.route('/',methods=['GET'], defaults={'shortname': None})
    # @nutritional_value_blueprint.route('/<shortname>',methods=['GET'])
    @token_required
    def get(self, auth_username, queryStringParameters, headers) -> Response:
        shortname = queryStringParameters.get("shortname", None)
        return json.dumps(self.get_nutritional_value.execute(shortname))

    # @nutritional_value_blueprint.route('/',methods=['POST'])
    @token_required
    def post(self, auth_username, body, headers) -> Response:
        return self.add_nutritional_value.execute(
            NutritionalValue(json.loads(body, object_hook=lambda d: SimpleNamespace(**d).__dict__)))

    # @nutritional_value_blueprint.route('/',methods=['DELETE'])
    @token_required
    def delete(self, auth_username, body, headers) -> Response:
        body = json.loads(body)
        shortname = body.get('shortname', None)
        return self.delete_nutritional_value.execute(shortname)

    @token_required
    def modify(self, auth_username, queryStringParameters, headers, body) -> Response:
        shortname = queryStringParameters.get('shortname', None)
        if shortname is None:
            raise Exception
        nutritional_value = self.get_nutritional_value.execute(shortname)
        body = json.loads(body)
        new_shortname = body.get("new_shortname", nutritional_value["shortname"])
        new_name = body.get("new_name", nutritional_value["name"])
        new_unit = body.get("new_unit", nutritional_value["unit"])

        self.delete_nutritional_value.execute(shortname)
        self.add_nutritional_value.execute(NutritionalValue(json.loads({"shortname": new_shortname, "name": new_name, "unit": new_unit}, object_hook=lambda d: SimpleNamespace(**d).__dict__)))
        return {}
