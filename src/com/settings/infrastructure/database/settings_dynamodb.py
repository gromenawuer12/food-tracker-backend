from ...domain.settings import Settings
from ....utils.log import Log
from ...domain.settings_database import SettingsDatabase
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key

from ...domain.settings_exception import SettingsException


class SettingsDynamoDB(SettingsDatabase):
    def __init__(self, client, log: Log):
        self.client = client
        self.table = self.client.Table('food-tracker')
        self.__log = log

    def create(self, settings):
        try:
            self.table.put_item(
                Item={
                    'PK': 'settings',
                    'SK': settings.shortname,
                    'settings': settings.serialize(),
                },
                ConditionExpression='attribute_not_exists(SK)'
            )
        except ClientError as e:
            if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
                raise SettingsException("Settings {0} can not be created because exist".format(settings.to_json()), 409)

    def find_all(self):
        response = self.table.query(
            ProjectionExpression="SK, settings",
            KeyConditionExpression=Key("PK").eq('settings')
        )

        if 'Items' not in response:
            return []
        return {'items': response['Items']}

    def find(self, shortname):
        self.__log.trace("DB settings find {0}", shortname)
        response = self.table.get_item(
            Key={
                'PK': 'settings',
                'SK': shortname
            },
            ProjectionExpression="settings"
        )
        if 'Item' not in response:
            self.__log.error("DB settings not found {0}", shortname)
            raise SettingsException("Settings value not found", 404)

        self.__log.trace("DB settings found {0}", response['Item'])
        return Settings(response['Item']['settings'])

    def delete(self, shortname):
        try:
            self.table.delete_item(
                Key={
                    'PK': 'settings',
                    'SK': shortname
                }
            )
        except ClientError:
            raise SettingsException("Something went wrong", 409)
