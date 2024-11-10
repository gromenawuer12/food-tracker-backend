import json

from ...domain.recipe_database import RecipeDatabase
from ...domain.recipe_exception import RecipeException
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key

PROJECTIONS = "#nm, description, products, nutritional_value, SK"


class RecipeDynamoDB(RecipeDatabase):
    def __init__(self, client, log):
        self.client = client
        self.table = self.client.Table('food-tracker')
        self.__log = log

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

    def find_all(self, query, last_evaluated_key, items_per_page):
        self.__log.trace('RecipeDynamoDB find_all: "{0}" [{1} : {2}]', query, last_evaluated_key, items_per_page)

        params = {
            'ProjectionExpression': PROJECTIONS,
            'ExpressionAttributeNames': {"#nm": "name"},
            'KeyConditionExpression': Key("PK").eq('recipe'),
        }
        if query:
            params['FilterExpression'] = 'contains(#nm, :nameQuery)'
            params['ExpressionAttributeValues'] = {':nameQuery': query}
        if not query and items_per_page:
            params['Limit'] = int(items_per_page)
        if not query and last_evaluated_key:
            params['ExclusiveStartKey'] = json.loads(last_evaluated_key)

        self.__log.trace(params)
        response = self.table.query(**params)

        if 'Items' not in response:
            self.__log.trace("Response {0}", response)
            raise RecipeException("Products not found", 404)

        result = {'items': response['Items']}
        if 'LastEvaluatedKey' in response:
            result['last_evaluated_key'] = response['LastEvaluatedKey']

        return result

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
