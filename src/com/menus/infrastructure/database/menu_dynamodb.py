import inject

from ....utils.log import Log
from ...domain.menu_database import MenuDatabase
from ...domain.menu_exception import MenuException
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key, Attr


class MenuDynamoDB(MenuDatabase):

    def __init__(self, client, log: Log):
        self.client = client
        self.table = self.client.Table('food-tracker')
        self.log = log

    def create(self, menu):
        try:
            self.table.put_item(
                Item={
                    'PK': 'menu#' + menu.username,
                    'SK': menu.date,
                    'username': menu.username,
                    'date': menu.date,
                    'recipes': menu.recipes,
                    'products': menu.products,
                    'nutritional_value': menu.nutritional_value
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
            ProjectionExpression="username, #dt, recipes, products, nutritional_value"
        )

        if 'Item' not in response:
            raise MenuException("Menu value not found", 404)

        return response['Item']

    def find_by_user_between(self, username, from_date, to_date):
        self.log.trace('MenuDynamoDB find_by_user_between: {0} {1} {2}', username, from_date, to_date)
        user_list = username.split(',')

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
                ProjectionExpression="#dt, username, recipes, nutritional_value, products",
            )
            results.extend(response['Items'])
        return results

    def find_all_between(self, from_date, to_date):
        partition_key_prefix = 'menu'

        response = self.table.scan(
            FilterExpression="begins_with(PK, :pk_prefix) AND #sk BETWEEN :start_date AND :end_date",
            ExpressionAttributeNames={
                "#sk": "SK",
                "#dt": "date"
            },
            ExpressionAttributeValues={
                ":pk_prefix": partition_key_prefix,
                ":start_date": from_date,
                ":end_date": to_date
            },
            ProjectionExpression="#dt, username, recipes, nutritional_value, products",
        )
        if 'Items' not in response:
            return []
        return response['Items']

    def find_by_username(self, username):
        self.log.trace('MenuDynamoDB find_by_username: {0}', username)

        response = self.table.query(
            KeyConditionExpression='#pk = :user',
            ExpressionAttributeNames={
                '#pk': 'PK',
                '#dt': 'date',
            },
            ExpressionAttributeValues={
                ':user': 'menu#' + username
            },
            ProjectionExpression="#dt, nutritional_value, username, recipes, products",
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
            FilterExpression=Key("PK").eq('menu#' + user) & (Key("SK").lt(date) | Key("SK").eq(date))
        )
        return response['Items']

    def find_lt_date(self, date):
        response = self.table.scan(
            ProjectionExpression="#dt, nutritional_value, username, recipes, products",
            ExpressionAttributeNames={"#dt": "date"},
            FilterExpression=Key("PK").begins_with('menu#') & (Key("SK").lt(date) | Key("SK").eq(date))
        )
        return response['Items']

    def find_all(self):
        response = self.table.scan(
            ProjectionExpression="#dt, nutritional_value, username, recipes, products",
            ExpressionAttributeNames={"#dt": "date"},
            FilterExpression=Key("PK").begins_with('menu#')
        )
        if 'Items' not in response:
            return []
        return response['Items']

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
