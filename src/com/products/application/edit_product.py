import inject
from ..domain.product import Product
from ..domain.product_database import ProductDatabase
from ..domain.product_exception import ProductException
from ...utils.log import Log


class EditProduct:
    @inject.autoparams()
    def __init__(self, database: ProductDatabase, log: Log):
        self.__database = database
        self.log = log

    def execute(self, sk, product: Product):
        product_old = Product(self.__database.find(sk))
        self.log.trace('edit_product: product={0}', product_old.to_json())

        self.__database.delete(sk)
        self.log.trace('edit_product: product with name={0} deleted', sk)
        try:
            self.log.trace('edit_product: creating product={0}', product.to_json())
            self.__database.create(product)
        except ProductException as product_exception:
            self.log.error('edit_product: error while adding, restoring to {0}', product_old.to_json())
            self.__database.create(product_old)
            raise product_exception
