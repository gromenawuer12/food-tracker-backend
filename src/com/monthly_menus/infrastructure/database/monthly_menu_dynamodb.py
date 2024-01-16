from ...domain.monthly_menu_database import MonthlyMenuDatabase
from ...domain.monthly_menu_exception import MonthlyMenuException
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key, Attr


class MonthlyMenuDynamoDB(MonthlyMenuDatabase):
    def __init__(self, client):
        self.client = client
        self.table = self.client.Table('food-tracker')

    def create(self, monthlyMenu):
        try:
            self.table.put_item(
                Item={
                    'PK': 'monthly_menu#' + monthlyMenu.username,
                    'SK': monthlyMenu.monthly_number,
                    'monthlyNumber': monthlyMenu.monthly_number,
                    'nutritional_value': monthlyMenu.nutritional_value
                },
                ConditionExpression='attribute_not_exists(SK)'
            )
        except ClientError as e:
            if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
                raise MonthlyMenuException("There is a conflict to create this resource", 409)
        return "Added"

    def findAll(self, username):
        response = self.table.scan(
            ProjectionExpression="monthlyNumber, nutritional_value",
            FilterExpression=Key("PK").eq('monthly_menu#' + username)
        )
        if 'Items' not in response:
            return []
        return response['Items']

    def find(self, username, monthlyNumber):
        response = self.table.get_item(
            Key={
                'PK': 'monthly_menu#' + username,
                'SK': monthlyNumber
            },
            ProjectionExpression="monthlyNumber, nutritional_value",
        )
        if 'Item' not in response:
            raise MonthlyMenuException("Menu not found", 404)
        return response['Item']

    def updateNutritionalValue(self, username, monthlyNumber, newNutritionalValue):
        self.table.update_item(
            Key={
                'PK': 'monthly_menu#' + username,
                'SK': monthlyNumber
            },
            UpdateExpression="SET nutritional_value = :val1",
            ExpressionAttributeValues={
                ':val1': newNutritionalValue
            }
        )
        return "Updated"
