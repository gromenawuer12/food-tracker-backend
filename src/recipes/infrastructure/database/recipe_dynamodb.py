import boto3
from recipes.domain.recipe_database import RecipeDatabase
from recipes.domain.recipe_exception import RecipeException
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key

class RecipeDynamoDB(RecipeDatabase):
    def __init__(self):
        self.client = boto3.resource('dynamodb', region_name='eu-west-3', endpoint_url='http://dynamodb:8000', aws_access_key_id='root', aws_secret_access_key='root')
        self.table = self.client.Table('food-tracker')

    def create(self, recipe):
        try:
            self.table.put_item(
                Item={
                    'PK': 'recipe',
                    'SK': recipe.name,
                    'name': recipe.name,
                    'products': recipe.products,
                },
                ConditionExpression='attribute_not_exists(SK)'
            )
        except ClientError as e:
            if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
                raise RecipeException("There is a conflict to create this resource",409)
        return "Added"

    def findAll(self):
        response = self.table.query(
             ProjectionExpression="#nm, products",
             ExpressionAttributeNames={"#nm": "name"},
             KeyConditionExpression=Key("PK").eq('recipe')
        )
        return response['Items']

    def find(self, name):
        response = self.table.get_item(
            Key={
                'PK': 'recipe',
                'SK': name
            },
            ProjectionExpression="#nm, products",
            ExpressionAttributeNames={"#nm": "name"},
        )
        return response['Item']

    def delete(self, name):
        try:
            self.table.delete_item(
                Key={
                    'PK': 'recipe',
                    'SK': name
                }
            )
        except ClientError:
            raise RecipeException("Something went wrong",409) 
        
        return "Deleted"