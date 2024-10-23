import json

import inject
from ...application.bot import Bot as BotApp
from ....utils.log import Log


def resolve(event):
    bot = Bot()
    return {'GET': bot.get,
            'POST': bot.get
            }[event['httpMethod']](event=event)


class Bot:
    @inject.autoparams()
    def __init__(self, bot_app: BotApp, log: Log):
        self.__reply = bot_app
        self.__log = log

    def get(self, event):
        self.__log.trace("--- BOT ---")
        self.__reply.execute(json.loads(event['body']))
