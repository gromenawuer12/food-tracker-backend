import boto3, sys
from products.domain.product_database import ProductDatabase
from products.domain.product_exception import ProductException
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key

class ProductDynamoDB(ProductDatabase):
    def __init__(self):
        self.client = boto3.resource('dynamodb', region_name='eu-west-3', endpoint_url='http://dynamodb:8000', aws_access_key_id='root', aws_secret_access_key='root')
        self.table = self.client.Table('food-tracker')

    def create(self, product):
        try:
            self.table.put_item(
                Item={
                    'PK': 'product',
                    'SK': product.name,
                    'name': product.name,
                    'nutritional_value': product.nutritional_value,
                    'description':product.description,
                    'supermarket':product.supermarket,
                },
                ConditionExpression='attribute_not_exists(SK)'
            )
        except ClientError as e:
            if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
                raise ProductException("There is a conflict to create this resource",409)
        return "Added"

    def findAll(self):
        response = self.table.query(
             ProjectionExpression="#nm, nutritional_value, description, quantity, supermarket, units",
             ExpressionAttributeNames={"#nm": "name"},
             KeyConditionExpression=Key("PK").eq('product')
        )
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
            raise ProductException("Something went wrong",409) 
        
        return "Deleted"