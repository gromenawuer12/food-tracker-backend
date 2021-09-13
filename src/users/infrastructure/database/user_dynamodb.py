import boto3, sys
from users.domain.user_database import UserDatabase
from werkzeug.security import generate_password_hash
from users.domain.user_exception import UserException
from botocore.exceptions import ClientError

class UserDynamoDB(UserDatabase):
    def __init__(self):
        self.client = boto3.resource('dynamodb', region_name='eu-west-3', endpoint_url='http://dynamodb:8000', aws_access_key_id='root', aws_secret_access_key='root')
        self.table = self.client.Table('food-tracker')

    def create(self, user):
        try:
            self.table.put_item(
                Item={
                    'PK': 'user',
                    'SK': user.username,
                    'username': user.username,
                    'password': user.password,
                    'role': user.role
                },
                ConditionExpression='attribute_not_exists(SK)'
            )
        except ClientError as e:
            if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
                raise UserException("There is a conflict to create this resource",409)
        return "Added"

    def find(self, username):
        response = self.table.get_item(
            Key={
                'PK': 'user',
                'SK': username
            }
        )
        return response['Item']
    
    def update(self,username,password,role):
        self.table.update_item(
            Key={
                'PK': 'user',
                'SK': username
            },
            UpdateExpression="SET password = :val1, #rl = :val2",
            ExpressionAttributeValues={
                ':val1': generate_password_hash(password,method='sha256'),
                ':val2': role
            },
            ExpressionAttributeNames={
                 '#rl': 'role'
             }
        )
        return "Updated"