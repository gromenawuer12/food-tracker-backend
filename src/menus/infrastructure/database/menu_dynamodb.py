from menus.domain.menu_database import MenuDatabase
from menus.domain.menu_exception import MenuException
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
                raise MenuException("There is a conflict to create this resource",409)
        return "Added"

    def findAll(self):
        response = self.table.scan(
            ProjectionExpression="#dt, recipes, nutritional_value, isLocked, PK",
            ExpressionAttributeNames={"#dt": "date"},
            FilterExpression=Key("PK").begins_with('menu')
        )
        return response['Items']

    def find(self, user, date):
        response = self.table.get_item(
            Key={
                'PK': 'menu#'+user,
                'SK': date
            },
            ProjectionExpression="#dt, recipes, nutritional_value",
            ExpressionAttributeNames={"#dt": "date"},
        )
        return response['Item']

    def findByDate(self, date):
        response = self.table.scan(
            ProjectionExpression="#dt, recipes, nutritional_value",
            ExpressionAttributeNames={"#dt": "date"},
            FilterExpression=Key("PK").begins_with('menu') & Key("SK").eq(date)
        )
        return response['Items']

    def findByUser(self, user):
        response = self.table.query(
             ProjectionExpression="#dt, recipes, nutritional_value",
            ExpressionAttributeNames={"#dt": "date"},
             KeyConditionExpression=Key("PK").eq('menu#'+user)
        )
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
            raise MenuException("Something went wrong",409) 
        
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