import json

from ...domain.product_database import ProductDatabase
from ...domain.product_exception import ProductException
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key


class ProductDynamoDB(ProductDatabase):
    def __init__(self, client, log):
        self.client = client
        self.table = self.client.Table('food-tracker')
        self.log = log

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
                    'recipe_name': product.recipe_name
                },
                ConditionExpression='attribute_not_exists(SK)'
            )
        except ClientError as e:
            if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
                raise ProductException("There is a conflict to create this resource", 409)

    def find_all(self, query, last_evaluated_key, items_per_page):
        self.log.trace('ProductDynamoDB find_all: "{0}" [{1} : {2}]', query, last_evaluated_key, items_per_page)

        params = {
            'ProjectionExpression': "#nm, SK, nutritional_value, description, quantity, supermarket, units, recipe_name",
            'ExpressionAttributeNames': {"#nm": "name"},
            'KeyConditionExpression': Key("PK").eq('product'),
        }
        if query:
            params['FilterExpression'] = 'contains(#nm, :nameQuery)'
            params['ExpressionAttributeValues'] = {':nameQuery': query}
        if not query and items_per_page:
            params['Limit'] = int(items_per_page)
        if not query and last_evaluated_key:
            params['ExclusiveStartKey'] = json.loads(last_evaluated_key)

        self.log.trace(params)
        response = self.table.query(**params)

        if 'Items' not in response:
            self.log.trace("Response {0}", response)
            raise ProductException("Products not found", 404)

        result = {'items': response['Items']}
        if 'LastEvaluatedKey' in response:
            result['last_evaluated_key'] = response['LastEvaluatedKey']

        return result

    def count(self):
        response = self.table.query(
            Select='COUNT',
            KeyConditionExpression=Key("PK").eq('product'),
        )
        self.log.trace('ProductDynamoDB count: {0}', response)

        if 'Count' not in response:
            raise ProductException("Product value not found", 404)

        return response['Count']

    def find(self, sk):
        response = self.table.get_item(
            Key={
                'PK': 'product',
                'SK': sk
            },
            ProjectionExpression="#nm, nutritional_value, description, quantity, supermarket, units, recipe_name",
            ExpressionAttributeNames={"#nm": "name"},
        )
        if 'Item' not in response:
            raise ProductException("Product value not found", 404)
        return response['Item']

    def delete(self, sk):
        try:
            self.table.delete_item(
                Key={
                    'PK': 'product',
                    'SK': sk
                }
            )
        except ClientError:
            raise ProductException("Something went wrong", 409)

        return "Deleted"
