from types import SimpleNamespace
import inject, json
from ...application.add_product import AddProduct
from ...application.get_product import GetProduct
from ...application.delete_product import DeleteProduct
from ...domain.product import Product
from ....resources.token.token_required_decorator import token_required
from ....utils.log import Log


def resolve(event):
    products_blueprint = ProductsBlueprint()
    return {"GET": products_blueprint.get,
            "POST": products_blueprint.post,
            "DELETE": products_blueprint.delete
            }[event['httpMethod']](event=event)


class ProductsBlueprint:
    @inject.autoparams()
    def __init__(self, get_product: GetProduct, add_product: AddProduct, delete_product: DeleteProduct):
        self.get_product = get_product
        self.add_product = add_product
        self.delete_product = delete_product

    @token_required
    def get(self, event):
        name = event['pathParameters'].get("name", None)
        return self.get_product.execute(name)

    @token_required
    def post(self, event):
        self.add_product.execute(
            Product(json.loads(event['body'], object_hook=lambda d: SimpleNamespace(**d).__dict__))
        )
        return {}

    @token_required
    def delete(self, event):
        body = json.loads(event['pathParameters'])
        name = body.get("name", None)
        return self.delete_product.execute(name)

    @token_required
    def modify(self, event):
        name = event['pathParameters'].get('name', None)
        if name is None:
            raise Exception
        product = self.get_product.execute(name)
        body = json.loads(event['pathParameters'])
        new_nutritional_value = body.get("new_nutritional_value", product["nutritional_value"])
        new_name = body.get("new_name", product["name"])
        new_description = body.get("new_description", product["description"])
        new_supermarket = body.get("new_supermarket", product["supermarket"])

        self.delete_product.execute.execute(name)
        self.add_product.execute.execute(Product(json.loads(
            '{"nutritional_value": new_nutritional_value, "name": new_name, "description": new_description, "supermarket": new_supermarket}',
            object_hook=lambda d: SimpleNamespace(**d).__dict__)))
        return {}
