from types import SimpleNamespace
import inject, json
from flask import Blueprint, Response, request
from ...application.add_unit import AddUnit
from ...application.get_unit import GetUnit
from ...application.delete_unit import DeleteUnit
from ...domain.unit import Unit
from resources.token.token_required_decorator import token_required


@inject.autoparams()
def create_units_blueprint(get_unit: GetUnit, add_unit: AddUnit, delete_unit: DeleteUnit) -> Blueprint:
    units_blueprint = Blueprint('units', __name__)

    @units_blueprint.route('/',methods=['GET'], defaults={'shortname': None})
    @units_blueprint.route('/<shortname>',methods=['GET'])
    @token_required
    def get(auth_username,shortname) -> Response:
        return json.dumps(get_unit.execute(shortname))

    @units_blueprint.route('/',methods=['POST'])
    @token_required
    def post(auth_username) -> Response:
        return add_unit.execute(Unit(json.loads(json.dumps(request.get_json()),object_hook=lambda d: SimpleNamespace(**d).__dict__)))
    
    @units_blueprint.route('/',methods=['DELETE'])
    @token_required
    def delete(auth_username) -> Response:
        return delete_unit.execute(request.get_json().get("shortname"))

    return units_blueprint