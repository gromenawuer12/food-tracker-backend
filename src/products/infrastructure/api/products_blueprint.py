from types import SimpleNamespace
import inject, json
from requests import Response
from ...application.add_product import AddProduct
from ...application.get_product import GetProduct
from ...application.delete_product import DeleteProduct
from ...domain.product import Product
from ....resources.token.token_required_decorator import token_required


def resolve(event):
    productsBlueprint = ProductsBlueprint()
    return eval({
                    "GET": "productsBlueprint.get(headers=event['headers'], pathParameters=event['pathParameters'])",
                    "POST": "productsBlueprint.post(headers=event['headers'], body=event['body'])",
                    "DELETE": "productsBlueprint.delete(headers=event['headers'], body=event['body'])"
                }[event['httpMethod']])


class ProductsBlueprint:
    @inject.autoparams()
    def __init__(self, get_product: GetProduct, add_product: AddProduct, delete_product: DeleteProduct):
        self.get_product = get_product
        self.add_product = add_product
        self.delete_product = delete_product

    # @products_blueprint.route('/',methods=['GET'], defaults={'name': None})
    # @products_blueprint.route('/<name>',methods=['GET'])
    @token_required
    def get(self, auth_username, pathParameters, headers) -> Response:
        name = pathParameters.get("name", None)
        return self.get_product.execute(name)

    # @products_blueprint.route('/',methods=['POST'])
    @token_required
    def post(self, auth_username, body, headers) -> Response:
        return self.add_product.execute(Product(json.loads(body, object_hook=lambda d: SimpleNamespace(**d).__dict__)))

    # @products_blueprint.route('/',methods=['DELETE'])
    @token_required
    def delete(self, auth_username, body, headers) -> Response:
        body = json.loads(body)
        name = body.get("name", None)
        return self.delete_product.execute(name)

    @token_required
    def modify(self, auth_username, pathParameters, headers, body) -> Response:
        name = pathParameters.get('name', None)
        if name is None:
            raise Exception
        product = self.get_product.execute(name)
        body = json.loads(body)
        new_nutritional_value = body.get("new_nutritional_value", product["nutritional_value"])
        new_name = body.get("new_name", product["name"])
        new_description = body.get("new_description", product["description"])
        new_supermarket = body.get("new_supermarket", product["supermarket"])

        self.delete_product.execute.execute(name)
        self.add_product.execute.execute(Product(json.loads('{"nutritional_value": new_nutritional_value, "name": new_name, "description": new_description, "supermarket": new_supermarket}', object_hook=lambda d: SimpleNamespace(**d).__dict__)))
        return {}