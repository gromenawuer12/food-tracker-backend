import re
from types import SimpleNamespace
import inject, json
from ...application.add_product import AddProduct
from ...application.count_product import CountProduct
from ...application.edit_product import EditProduct
from ...application.get_product import GetProduct
from ...application.delete_product import DeleteProduct
from ...domain.product import Product
from ....resources.token.token_required_decorator import token_required
from ....utils.log import Log


def resolve(event):
    products_blueprint = ProductsBlueprint()
    if re.search('/products/count', event['path']):
        return products_blueprint.length(event=event)

    return {"GET": products_blueprint.get,
            "POST": products_blueprint.post,
            "PUT": products_blueprint.put,
            "DELETE": products_blueprint.delete
            }[event['httpMethod']](event=event)


class ProductsBlueprint:
    @inject.autoparams()
    def __init__(self, get_product: GetProduct, add_product: AddProduct, delete_product: DeleteProduct,
                 count_product: CountProduct, edit_product: EditProduct, log: Log):
        self.get_product = get_product
        self.add_product = add_product
        self.delete_product = delete_product
        self.count_product = count_product
        self.edit_product = edit_product
        self.log = log

    @token_required
    def get(self, event):
        name = event['pathParameters'].get('name', None)

        query_string_parameters = event['queryStringParameters'];
        items_per_page = None
        last_evaluated_key = None
        if query_string_parameters:
            items_per_page = query_string_parameters.get('itemsPerPage', None)
            last_evaluated_key = query_string_parameters.get('last_evaluated_key', None)

        return self.get_product.execute(name, last_evaluated_key, items_per_page)

    @token_required
    def length(self, event):
        return self.count_product.execute()

    @token_required
    def post(self, event):
        self.add_product.execute(
            Product(json.loads(event['body'], object_hook=lambda d: SimpleNamespace(**d).__dict__))
        )
        return {}

    @token_required
    def delete(self, event):
        name = json.loads(event['body']).get("name", None)
        return self.delete_product.execute(name)

    @token_required
    def put(self, event):
        self.log.debug('put: proxy={0}', json.dumps(event['pathParameters']['proxy']))
        name = event['pathParameters']['proxy'].split('/')[1]
        self.log.trace('put: shortname={0}', name)

        if name is None:
            raise Exception

        body = json.loads(event['body'])
        self.log.trace('put: body={0}', body)

        self.edit_product.execute(name, Product(body))
