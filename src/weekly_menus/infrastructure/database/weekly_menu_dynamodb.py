from ...domain.weekly_menu_database import WeeklyMenuDatabase
from ...domain.weekly_menu_exception import WeeklyMenuException
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key, Attr

class WeeklyMenuDynamoDB(WeeklyMenuDatabase):
    def __init__(self,client):
        self.client = client
        self.table = self.client.Table('food-tracker')

    def create(self, weeklyMenu):
        try:
            self.table.put_item(
                Item={
                    'PK': 'weekly_menu#'+weeklyMenu.user,
                    'SK': weeklyMenu.weekly_number,
                    'weeklyNumber': weeklyMenu.weekly_number,
                    'nutritional_value': weeklyMenu.nutritional_value
                },
                ConditionExpression='attribute_not_exists(SK)'
            )
        except ClientError as e:
            if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
                raise WeeklyMenuException("There is a conflict to create this resource",409)
        return "Added"

    def findAll(self,user):
        response = self.table.scan(
            ProjectionExpression="weeklyNumber, nutritional_value",
            FilterExpression=Key("PK").eq('weekly_menu#'+user)
        )
        if 'Items' not in response:
            return []
        return response['Items']

    def find(self, user, weeklyNumber):
        response = self.table.get_item(
            Key={
                'PK': 'weekly_menu#'+user,
                'SK': weeklyNumber
            },
            ProjectionExpression="weeklyNumber, nutritional_value",
        )
        if 'Item' not in response:
            raise WeeklyMenuException("Menu not found", 404)
        return response['Item']

    def updateNutritionalValue(self,user,weeklyNumber,newNutritionalValue):
        self.table.update_item(
            Key={
                'PK': 'weekly_menu#'+user,
                'SK': weeklyNumber
            },
            UpdateExpression="SET nutritional_value = :val1",
            ExpressionAttributeValues={
                ':val1': newNutritionalValue
            }
        )
        return "Updated"