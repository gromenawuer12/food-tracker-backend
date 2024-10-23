import json
import os
import sys

import inject
import requests

from .menu import Menu
from ..domain.message import Message
from ...utils.log import Log

TELEGRAM_TOKEN = os.environ['TELEGRAM_TOKEN']

class Bot:
    @inject.autoparams()
    def __init__(self, log: Log, menu: Menu):
        self.__log = log
        self.__commands = {
            "/start": lambda chat_id, command: Message(chat_id, 'Choose an option', json.dumps({
                'inline_keyboard': [[
                    {'text': 'Menus', 'callback_data': '/menu get'},
                ]]
            })),
            '/help': json.dumps({
                'inline_keyboard': [[
                    {'text': 'TODAY', 'callback_data': 'today'},
                ]]
            }),
            '/menu': menu.resolver
        }

    def execute(self, body):
        chat_id = ''
        try:
            self.__log.trace("--- BOT EXECUTE ---")

            if 'message' in body:
                chat_id = body['message']['chat']['id']
                message_text = body['message']['text']
                self.__log.trace('Message {0} {1}', chat_id, message_text)

                message_to_send = self.get_command(chat_id, message_text)
                self.send_message(message_to_send)

            elif 'callback_query' in body:
                callback_query = body['callback_query']
                chat_id = callback_query['message']['chat']['id']
                callback_data = callback_query['data']
                self.__log.trace('CallbackQuery {0} {1}', chat_id, callback_data)

                message_to_send = self.get_command(chat_id, callback_data)
                self.send_message(message_to_send)
        except Exception as error:
            ex_type, ex_value, ex_traceback = sys.exc_info()
            self.__log.error('Error bot: {0} {1} {2}'.format(ex_type, str(error), ex_traceback))
            self.send_message(Message(chat_id, 'Something wrong happens 😨'))


    def send_message(self, message: Message):
        self.__log.trace("ID {0} TEXT {1}", message.chat_id, message.text)
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        self.__log.trace("Payload {0}", message.payload)
        response = requests.post(url, json=message.payload)
        self.__log.trace("Response {0}", response.json())
        return response.json()

    def get_command(self, chat_id, command) -> Message:
        lower_command = command.lower().split()[0]
        if lower_command in self.__commands:
            self.__log.trace("GET_COMMAND {0}", lower_command)
            return self.__commands[lower_command](chat_id, command)
        else:
            return Message(chat_id, 'Sorry I can not understand 😓')