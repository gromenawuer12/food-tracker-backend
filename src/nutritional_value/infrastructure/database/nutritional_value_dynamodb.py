from nutritional_value.domain.nutritional_value_database import NutritionalValueDatabase
from nutritional_value.domain.nutritional_value_exception import NutritionalValueException
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key

class NutritionalValueDynamoDB(NutritionalValueDatabase):
    def __init__(self,client):
        self.client = client
        self.table = self.client.Table('food-tracker')

    def create(self, nutritionalValue):
        try:
            self.table.put_item(
                Item={
                    'PK': 'nutritional value',
                    'SK': nutritionalValue.shortname,
                    'shortname': nutritionalValue.shortname,
                    'name': nutritionalValue.name,
                    'unit': nutritionalValue.unit
                },
                ConditionExpression='attribute_not_exists(SK)'
            )
        except ClientError as e:
            if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
                raise NutritionalValueException("There is a conflict to create this resource",409)
        return "Added"

    def findAll(self):
        response = self.table.query(
             ProjectionExpression="shortname, #nm, #un",
             ExpressionAttributeNames={"#nm": "name","#un":"unit"},
             KeyConditionExpression=Key("PK").eq('nutritional value')
        )
        return response['Items']

    def find(self, shortname):
        response = self.table.get_item(
            Key={
                'PK': 'nutritional value',
                'SK': shortname
            },
            ProjectionExpression="shortname, #nm, #un",
            ExpressionAttributeNames={"#nm": "name","#un":"unit"},
        )
        return response['Item']

    def delete(self, shortname):
        try:
            self.table.delete_item(
                Key={
                    'PK': 'nutritional value',
                    'SK': shortname
                }
            )
        except ClientError:
            raise NutritionalValueException("Something went wrong",409) 
        
        return "Deleted"