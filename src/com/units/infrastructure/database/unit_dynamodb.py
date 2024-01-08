import json

from ...domain.unit_database import UnitDatabase
from ...domain.unit_exception import UnitException
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key


class UnitDynamoDB(UnitDatabase):
    def __init__(self, client):
        self.client = client
        self.table = self.client.Table('food-tracker')

    def create(self, unit):
        try:
            self.table.put_item(
                Item={
                    'PK': 'unit',
                    'SK': unit.shortname,
                    'shortname': unit.shortname,
                    'name': unit.name,
                },
                ConditionExpression='attribute_not_exists(SK)'
            )
        except ClientError as e:
            if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
                raise UnitException("Unit {0} can not be created because exist".format(unit.to_json()), 409)

    def find_all(self):
        response = self.table.query(
            ProjectionExpression="shortname, #nm",
            ExpressionAttributeNames={"#nm": "name"},
            KeyConditionExpression=Key("PK").eq('unit')
        )

        if 'Items' not in response:
            return []
        return {'items': response['Items']}

    def find(self, shortname):
        response = self.table.get_item(
            Key={
                'PK': 'unit',
                'SK': shortname
            },
            ProjectionExpression="shortname, #nm",
            ExpressionAttributeNames={"#nm": "name"},
        )
        if 'Item' not in response:
            raise UnitException("Unit value not found", 404)
        return response['Item']

    def delete(self, shortname):
        try:
            self.table.delete_item(
                Key={
                    'PK': 'unit',
                    'SK': shortname
                }
            )
        except ClientError:
            raise UnitException("Something went wrong", 409)
