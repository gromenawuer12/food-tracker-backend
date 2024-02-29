from ...domain.recipe_database import RecipeDatabase
from ...domain.recipe_exception import RecipeException
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key

PROJECTIONS = "#nm, description, products, nutritional_value, SK"


class RecipeDynamoDB(RecipeDatabase):
    def __init__(self, client):
        self.client = client
        self.table = self.client.Table('food-tracker')

    def create(self, recipe):
        try:
            self.table.put_item(
                Item={
                    'PK': 'recipe',
                    'SK': recipe.name,
                    'name': recipe.name,
                    'description': recipe.description,
                    'products': recipe.products,
                    'nutritional_value': recipe.nutritional_value
                },
                ConditionExpression='attribute_not_exists(SK)'
            )
        except ClientError as e:
            if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
                raise RecipeException("There is a conflict to create this resource", 409)

    def find_all(self):
        response = self.table.query(
            ProjectionExpression=PROJECTIONS,
            ExpressionAttributeNames={"#nm": "name"},
            KeyConditionExpression=Key("PK").eq('recipe')
        )
        if 'Items' not in response:
            return []

        return {'items': response['Items']}

    def find(self, sk):
        response = self.table.get_item(
            Key={
                'PK': 'recipe',
                'SK': sk
            },
            ProjectionExpression=PROJECTIONS,
            ExpressionAttributeNames={"#nm": "name"},
        )
        if 'Item' not in response:
            raise RecipeException("Recipe value not found", 404)

        return response['Item']

    def delete(self, sk):
        try:
            self.table.delete_item(
                Key={
                    'PK': 'recipe',
                    'SK': sk
                }
            )
        except ClientError:
            raise RecipeException("Something went wrong", 409)
