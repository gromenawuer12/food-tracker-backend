import json

import inject

from ...application.add_settings import AddSettings
from ...application.get_settings import GetSettings
from ...domain.settings import Settings
from ....resources.token.token_required_decorator import token_required
from ....utils.log import Log


def resolve(event):
    settings_blueprint = SettingsBlueprint()
    return {
        "GET": settings_blueprint.get,
        "POST": settings_blueprint.post
    }[event['httpMethod']](event=event)


class SettingsBlueprint:
    @inject.autoparams()
    def __init__(self, get_settings: GetSettings, add_settings: AddSettings, log: Log):
        self.__get_settings = get_settings
        self.__add_settings = add_settings
        self.__log = log

    @token_required
    def get(self, event):
        self.__log.debug('get settings')
        self.__log.debug('get settings: proxy={0}', json.dumps(event['pathParameters']['proxy']))
        shortname = event['pathParameters']['proxy'].split('/')[1]
        return self.__get_settings.execute(shortname)

    @token_required
    def post(self, event):
        self.__log.debug('post settings')
        body = json.loads(event['body'])
        self.__log.debug(body)
        self.__add_settings.execute(Settings(body))
