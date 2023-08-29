from ...domain.product_database import ProductDatabase
from ...domain.product_exception import ProductException
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key


class ProductDynamoDB(ProductDatabase):
    def __init__(self, client):
        self.client = client
        self.table = self.client.Table('food-tracker')

    def create(self, product):
        try:
            self.table.put_item(
                Item={
                    'PK': 'product',
                    'SK': product.name,
                    'name': product.name,
                    'nutritional_value': product.nutritional_value,
                    'description': product.description,
                    'supermarket': product.supermarket,
                },
                ConditionExpression='attribute_not_exists(SK)'
            )
        except ClientError as e:
            if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
                raise ProductException("There is a conflict to create this resource", 409)

    def findAll(self):
        response = self.table.query(
            ProjectionExpression="#nm, nutritional_value, description, quantity, supermarket, units",
            ExpressionAttributeNames={"#nm": "name"},
            KeyConditionExpression=Key("PK").eq('product')
        )
        if 'Items' not in response:
            raise []
        return response['Items']

    def find(self, name):
        response = self.table.get_item(
            Key={
                'PK': 'product',
                'SK': name
            },
            ProjectionExpression="#nm, nutritional_value, description, quantity, supermarket, units",
            ExpressionAttributeNames={"#nm": "name"},
        )
        if 'Item' not in response:
            raise ProductException("Product value not found", 404)
        return response['Item']

    def delete(self, name):
        try:
            self.table.delete_item(
                Key={
                    'PK': 'product',
                    'SK': name
                }
            )
        except ClientError:
            raise ProductException("Something went wrong", 409)

        return "Deleted"
