from ...domain.menu_database import MenuDatabase
from ...domain.menu_exception import MenuException
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key, Attr

class MenuDynamoDB(MenuDatabase):
    def __init__(self,client):
        self.client = client
        self.table = self.client.Table('food-tracker')

    def create(self, menu):
        try:
            self.table.put_item(
                Item={
                    'PK': 'menu#'+menu.user,
                    'SK': menu.date,
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
        return "Added"

    def find(self, user, fromDate, toDate):
        if user.indexOf(',') > -1:
            user_list = user.split(',')
            user_list_parsed = ' OR PK = menu#'.join(user_list)
            user_list_parsed = 'PK = menu#' + user_list_parsed
        else:
            user_list_parsed = 'PK = ' + user
        response = self.table.query(
            KeyConditionExpression=user_list_parsed + ' AND #sk BETWEEN :start_date AND :end_date',
            ExpressionAttributeNames={
                '#sk': 'SK',
                '#dt': 'date'
            },
            ExpressionAttributeValues={
                ':start_date': fromDate,
                ':end_date': toDate
            },
            ProjectionExpression="#dt, recipes, nutritional_value, isLocked, PK",
        )
        if 'Items' not in response:
            return []
        return response['Items']

    def findByDate(self, fromDate, toDate):
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

    def findByUser(self, user):
        response = self.table.query(
             ProjectionExpression="#dt, recipes, nutritional_value, isLocked, PK",
             ExpressionAttributeNames={"#dt": "date"},
             KeyConditionExpression=Key("PK").eq('menu#'+user)
        )
        if 'Items' not in response:
            return []
        return response['Items']
        
    def delete(self, user, date):
        try:
            self.table.delete_item(
                Key={
                    'PK': 'menu#'+user,
                    'SK': date
                }
            )
        except ClientError:
            raise MenuException("Something went wrong", 409)
        
        return "Deleted"
    
    def findUnlocked(self,user,date):
        response = self.table.scan(
            ProjectionExpression="#dt, nutritional_value",
            ExpressionAttributeNames={"#dt": "date"},
            FilterExpression=Key("PK").eq('menu#'+user) & (Key("SK").lt(date) | Key("SK").eq(date)) & Attr("isLocked").eq(False)
        )
        return response['Items']

    def updateIsLocked(self,user,date):
        self.table.update_item(
            Key={
                'PK': 'menu#'+user,
                'SK': date
            },
            UpdateExpression="SET isLocked = :val1",
            ExpressionAttributeValues={
                ':val1': True
            }
        )
        return "Updated"