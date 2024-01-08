from ...domain.nutritional_value_database import NutritionalValueDatabase
from ...domain.nutritional_value_exception import NutritionalValueException
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key


class NutritionalValueDynamoDB(NutritionalValueDatabase):
    def __init__(self, client, log):
        self.client = client
        self.table = self.client.Table('food-tracker')
        self.log = log
        self.pk = 'nutritional_value'

    def create(self, nutritional_value):
        try:
            self.table.put_item(
                Item={
                    'PK': self.pk,
                    'SK': nutritional_value.shortname,
                    'shortname': nutritional_value.shortname,
                    'name': nutritional_value.name,
                    'unit': nutritional_value.unit
                },
                ConditionExpression='attribute_not_exists(SK)'
            )
        except ClientError as e:
            if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
                raise NutritionalValueException("NutritionalValue {0} can not be created because exist"
                                                .format(nutritional_value.to_json()), 409)

    def findAll(self):
        response = self.table.query(
            ProjectionExpression="shortname, #nm, #un",
            ExpressionAttributeNames={"#nm": "name", "#un": "unit"},
            KeyConditionExpression=Key("PK").eq(self.pk)
        )
        if 'Items' not in response:
            return []
        return {'items': response['Items']}

    def find(self, shortname):
        response = self.table.get_item(
            Key={
                'PK': self.pk,
                'SK': shortname
            },
            ProjectionExpression="shortname, #nm, #un",
            ExpressionAttributeNames={"#nm": "name", "#un": "unit"},
        )
        if 'Item' not in response:
            raise NutritionalValueException("Nutritional value not found", 404)
        return response['Item']

    def delete(self, shortname):
        try:
            self.table.delete_item(
                Key={
                    'PK': self.pk,
                    'SK': shortname
                }
            )
        except ClientError:
            raise NutritionalValueException("Something went wrong", 409)