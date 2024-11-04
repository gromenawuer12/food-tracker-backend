import json
import os
import sys

import inject
import requests

from .menu import Menu
from .weekly_menu import WeeklyMenu
from ..domain.message_response import MessageResponse
from ..domain.message_request import MessageRequest
from ...utils.log import Log

TELEGRAM_TOKEN = os.environ['TELEGRAM_TOKEN']

class Bot:
    @inject.autoparams()
    def __init__(self, log: Log, menu: Menu, weekly_menu: WeeklyMenu):
        self.__log = log
        self.__commands = {
            "/start": lambda message_request: MessageResponse(message_request.chat_id, 'Choose an option', json.dumps({
                'inline_keyboard': [
                    [{'text': 'Menus', 'callback_data': f'{message_request.message_id} /menu get'}],
                    [{'text': 'WeeklyMenus', 'callback_data': f'{message_request.message_id} /weekly-menu get'}]
                ]
            }), message_id = message_request.message_id),
            '/help': json.dumps({
                'inline_keyboard': [[
                    {'text': 'TODAY', 'callback_data': 'today'},
                ]]
            }),
            '/menu': menu.resolver,
            '/weekly-menu': weekly_menu.resolver
        }

    def execute(self, body):
        chat_id = ''
        try:
            self.__log.trace("--- BOT EXECUTE ---")

            if 'message' in body:
                chat_id = body['message']['chat']['id']
                message_text = body['message']['text']
                self.__log.trace('Message {0} {1}', chat_id, message_text)

                message_request = self.get_message_request(chat_id, message_text)
                if not message_request.message_id:
                    response = self.send_message(MessageResponse(chat_id, "loading\.\.\."))
                    message_request = self.get_message_request(chat_id, f"{response['result']['message_id']} {message_text}")

                self.send_message(self.get_command(message_request))

            elif 'callback_query' in body:
                callback_query = body['callback_query']
                chat_id = callback_query['message']['chat']['id']
                callback_data = callback_query['data']
                self.__log.trace('CallbackQuery {0} {1}', chat_id, callback_data)

                message_request = self.get_message_request(chat_id, callback_data)
                if not message_request.message_id:
                    response = self.send_message(MessageResponse(chat_id, "loading\.\.\."))
                    message_request = self.get_message_request(chat_id, f"{response['result']['message_id']} {callback_data}")

                self.send_message(self.get_command(message_request))

        except Exception as error:
            ex_type, ex_value, ex_traceback = sys.exc_info()
            self.__log.error('Error bot: {0} {1} {2}'.format(ex_type, str(error), ex_traceback))
            self.send_message(MessageResponse(chat_id, 'Something wrong happens 😨'))


    def send_message(self, message: MessageResponse):
        self.__log.trace("ID {0} TEXT {1}", message.chat_id, message.text)
        action = 'editMessageText' if message.message_id else 'sendMessage'
        self.__log.trace("ACTION {0}", action)
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/{action}"

        self.__log.trace("Payload {0}", message.payload)
        response = requests.post(url, json=message.payload)

        self.__log.trace("Response {0}", response.json())
        return response.json()

    def get_command(self, message_request: MessageRequest) -> MessageResponse:
        self.__log.trace("GET_COMMAND {0}", message_request.command_parts[0])
        if message_request.command_parts[0] in self.__commands:
            return self.__commands[message_request.command_parts[0]](message_request)
        else:
            return MessageResponse(message_request.chat_id, 'Sorry I can not understand 😓')

    def get_message_request(self, chat_id, command):
        return MessageRequest(chat_id, command)