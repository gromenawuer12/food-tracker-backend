from ...domain.menu_database import MenuDatabase
from ...domain.menu_exception import MenuException
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key, Attr


class MenuDynamoDB(MenuDatabase):
    def __init__(self, client):
        self.client = client
        self.table = self.client.Table('food-tracker')

    def create(self, menu):
        try:
            self.table.put_item(
                Item={
                    'PK': 'menu#' + menu.username,
                    'SK': menu.date,
                    'username': menu.username,
                    'date': menu.date,
                    'recipes': menu.recipes,
                    'nutritional_value': menu.nutritional_value,
                    'isLocked': menu.isLocked
                },
                ConditionExpression='attribute_not_exists(SK)'
            )
        except ClientError as e:
            if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
                raise MenuException("There is a conflict to create this resource", 409)

    def find(self, username, date):
        response = self.table.get_item(
            Key={
                'PK': 'menu#' + username,
                'SK': date
            },
            ExpressionAttributeNames={"#dt": "date"},
            ProjectionExpression="username, #dt, recipes, nutritional_value, isLocked"
        )

        if 'Item' not in response:
            raise MenuException("Menu value not found", 404)

        return response['Item']

    def find_by_user_between(self, user, from_date, to_date):
        user_list = user.split(',')

        results = []
        for user in user_list:
            response = self.table.query(
                KeyConditionExpression='#pk = :user AND #sk BETWEEN :start_date AND :end_date',
                ExpressionAttributeNames={
                    '#pk': 'PK',
                    '#sk': 'SK',
                    '#dt': 'date',
                },
                ExpressionAttributeValues={
                    ':start_date': from_date,
                    ':end_date': to_date,
                    ':user': 'menu#' + user
                },
                ProjectionExpression="#dt, recipes, nutritional_value, isLocked, PK",
            )
            results.extend(response['Items'])
        return results

    def find_between(self, fromDate, toDate):
        partition_key_prefix = 'menu'

        response = self.table.scan(
            FilterExpression="begins_with(PK, :pk_prefix) AND #sk BETWEEN :start_date AND :end_date",
            ExpressionAttributeNames={
                "#sk": "SK"
            },
            ExpressionAttributeValues={
                ":pk_prefix": partition_key_prefix,
                ":start_date": fromDate,
                ":end_date": toDate
            }
        )
        if 'Items' not in response:
            return []
        return response['Items']

    def find_by_user(self, user):
        response = self.table.query(
            ProjectionExpression="#dt, recipes, nutritional_value, isLocked, PK",
            ExpressionAttributeNames={"#dt": "date"},
            KeyConditionExpression=Key("PK").eq('menu#' + user)
        )
        if 'Items' not in response:
            return []
        return response['Items']

    def delete(self, username, date):
        try:
            self.table.delete_item(
                Key={
                    'PK': 'menu#' + username,
                    'SK': date
                }
            )
        except ClientError:
            raise MenuException("Something went wrong", 409)

    def find_unlocked_by_user(self, user, date):
        response = self.table.scan(
            ProjectionExpression="#dt, nutritional_value",
            ExpressionAttributeNames={"#dt": "date"},
            FilterExpression=Key("PK").eq('menu#' + user) & (Key("SK").lt(date) | Key("SK").eq(date)) & Attr(
                "isLocked").eq(False)
        )
        return response['Items']

    def find_unlocked(self):
        response = self.table.scan(
            ProjectionExpression="#dt, nutritional_value, username, recipes",
            ExpressionAttributeNames={"#dt": "date"},
            FilterExpression=Key("PK").begins_with('menu#') & Attr("isLocked").eq(False)
        )
        return {'items': response['Items']}

    def updateIsLocked(self, user, date):
        self.table.update_item(
            Key={
                'PK': 'menu#' + user,
                'SK': date
            },
            UpdateExpression="SET isLocked = :val1",
            ExpressionAttributeValues={
                ':val1': True
            }
        )
        return "Updated"
