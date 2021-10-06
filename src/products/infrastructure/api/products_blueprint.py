from types import SimpleNamespace
import inject, json
from flask import Blueprint, Response, request
from ...application.add_product import AddProduct
from ...application.get_product import GetProduct
from ...application.delete_product import DeleteProduct
from ...domain.product import Product
from resources.token.token_required_decorator import token_required


@inject.autoparams()
def create_products_blueprint(get_product: GetProduct, add_product: AddProduct, delete_product: DeleteProduct) -> Blueprint:
    products_blueprint = Blueprint('products', __name__)

    @products_blueprint.route('/',methods=['GET'], defaults={'name': None})
    @products_blueprint.route('/<name>',methods=['GET'])
    @token_required
    def get(auth_username,name) -> Response:
        return json.dumps(get_product.execute(name))

    @products_blueprint.route('/',methods=['POST'])
    @token_required
    def post(auth_username) -> Response:
        return add_product.execute(Product(json.loads(json.dumps(request.get_json()),object_hook=lambda d: SimpleNamespace(**d).__dict__)))
    
    @products_blueprint.route('/',methods=['DELETE'])
    @token_required
    def delete(auth_username) -> Response:
        return delete_product.execute(request.get_json().get("name"))

    return products_blueprint