from ...domain.weekly_menu_database import WeeklyMenuDatabase
from ...domain.weekly_menu_exception import WeeklyMenuException
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key, Attr


class WeeklyMenuDynamoDB(WeeklyMenuDatabase):
    def __init__(self, client):
        self.client = client
        self.table = self.client.Table('food-tracker')

    def create(self, weekly_menu):
        try:
            self.table.put_item(
                Item={
                    'PK': 'weekly_menu#' + weekly_menu.username,
                    'SK': weekly_menu.weekly_number,
                    'username': weekly_menu.username,
                    'menus': weekly_menu.menus,
                    'weekly_number': weekly_menu.weekly_number,
                    'nutritional_value': weekly_menu.nutritional_value
                },
                ConditionExpression='attribute_not_exists(SK)'
            )
        except ClientError as e:
            if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
                raise WeeklyMenuException("There is a conflict to create this resource", 409)

    def findAll(self, username):
        response = self.table.scan(
            ProjectionExpression="weekly_number, nutritional_value",
            FilterExpression=Key("PK").eq('weekly_menu#' + username)
        )
        if 'Items' not in response:
            return []
        return response['Items']

    def find(self, username, weekly_number):
        response = self.table.get_item(
            Key={
                'PK': 'weekly_menu#' + username,
                'SK': weekly_number
            },
            ProjectionExpression="weekly_number, nutritional_value, menus",
        )
        if 'Item' not in response:
            raise WeeklyMenuException("WeeklyMenu not found", 404)
        return response['Item']

    def update_nutritional_value(self, username, weekly_number, new_nutritional_value, menus):
        self.table.update_item(
            Key={
                'PK': 'weekly_menu#' + username,
                'SK': weekly_number
            },
            UpdateExpression="SET nutritional_value = :val1, menus = :val2",
            ExpressionAttributeValues={
                ':val1': new_nutritional_value,
                ':val2': menus
            }
        )
