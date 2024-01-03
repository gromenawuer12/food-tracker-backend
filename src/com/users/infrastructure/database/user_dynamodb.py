from ...domain.user_database import UserDatabase
from ...domain.user_exception import UserException
from botocore.exceptions import ClientError


class UserDynamoDB(UserDatabase):
    def __init__(self, client, log):
        self.client = client
        self.table = self.client.Table('food-tracker')
        self.log = log

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
                raise UserException("There is a conflict to create this resource", 409)
        return "Added"

    def find(self, username):
        self.log.trace('UserDynamoDB find: {0}', username)
        response = self.table.get_item(
            Key={
                'PK': 'user',
                'SK': username
            },
            ProjectionExpression="username, password"
        )

        if 'Item' not in response:
            raise UserException("User not found", 404)

        self.log.trace('UserDynamoDB found')

        return response['Item']

    def findAll(self):
        response = self.table.query(
            KeyConditionExpression='PK = :pk',
            ExpressionAttributeValues={
                ':pk': 'user'
            },
            ProjectionExpression="username",
        )
        if 'Items' not in response:
            return []
        return response['Items']

    """
    ':val1': generate_password_hash(password,method='sha256'),
    """

    def update(self, username, password, role):
        self.table.update_item(
            Key={
                'PK': 'user',
                'SK': username
            },
            UpdateExpression="SET password = :val1, #rl = :val2",
            ExpressionAttributeValues={
                ':val1': password,
                ':val2': role
            },
            ExpressionAttributeNames={
                '#rl': 'role'
            }
        )
        return "Updated"
