import datetime
import json

import inject

from .format import escape_markdown_v2
from ..domain.message_request import MessageRequest
from ..domain.message_response import MessageResponse
from ...menus.domain.menu_database import MenuDatabase
from ...menus.domain.menu_exception import MenuException
from ...settings.application.get_settings import GetSettings
from ...utils.log import Log

MENU_COMMAND = '/menus'

class Menu:
    @inject.autoparams()
    def __init__(self, log: Log, menu_db: MenuDatabase, get_settings: GetSettings):
        self.__log = log
        self.__menu_db = menu_db
        self.__get_settings = get_settings
        self.__commands = {
            'get': self.get
        }

    def resolver(self, message_request: MessageRequest):
        self.__log.trace('Menu resolver {0}', message_request)
        return self.__commands[message_request.command_parts[1]](message_request)

    def get(self, message_request: MessageRequest):
        self.__log.trace('Bot Menu' + message_request.to_string())
        if message_request.command_parts_length == 2:
            return self.request_users(message_request)

        if message_request.command_parts_length == 3:
            return self.request_days(message_request)

        try:
            return MessageResponse(message_request.chat_id, self.format(self.__menu_db.find(message_request.command_parts[2], message_request.command_parts[3])), message_id = message_request.message_id)
        except MenuException:
            date = message_request.command_parts[3].replace('-', '\-')
            return MessageResponse(message_request.chat_id, f'There are not a menu for {message_request.command_parts[2]} on {date}', message_id = message_request.message_id)

    def today(self):
        return self.format(self.__menu_db.find('elias', datetime.date.today().strftime("%Y-%m-%d")))

    def format(self, data):
        self.__log.trace('format {0}', data)
        mensaje = f"📅 *Fecha:* {escape_markdown_v2(data['date'])}\n"
        mensaje += f"👤 *Usuario:* {escape_markdown_v2(data['username'])}\n\n"
        mensaje += "*Valores Nutricionales:*\n"
        for item in data['nutritional_value']:
            mensaje += f" \- {escape_markdown_v2(item['name'])}: {escape_markdown_v2(item['value'])} {escape_markdown_v2(item['unit'])}\n"

        mensaje += "\n*Productos:*\n"
        parts_of_day = self.__get_settings.execute('settings_v1').get('partsOfDay', '').split(',')
        if isinstance(data['products'], dict):
            for part_of_day in parts_of_day:
                comida = part_of_day
                items = data['products'].get(part_of_day, None)
                if items:
                    mensaje += f"🍽️ *{escape_markdown_v2(comida)}:*\n"
                    for item in items:
                        if 'recipe_name' in item and item['recipe_name']:
                            mensaje += f"   \- {escape_markdown_v2(item['name'])} \(Cantidad: {escape_markdown_v2(item['value'])} \- Receta: {escape_markdown_v2(item['recipe_name'])}\)\n"
                        else:
                            mensaje += f"   \- {escape_markdown_v2(item['name'])} \(Cantidad: {escape_markdown_v2(item['value'])}\)\n"

        return mensaje

    def request_users(self, message_request: MessageRequest):
        return MessageResponse(message_request.chat_id, 'Choose user:', json.dumps({
            'inline_keyboard': [[
                {'text': 'Elias', 'callback_data': f'{message_request.message_id} {MENU_COMMAND} get elias'},
                {'text': 'Roma', 'callback_data': f'{message_request.message_id} {MENU_COMMAND} get roma'},
            ]]
        }), message_id = message_request.message_id)

    def request_days(self, message_request):
        self.__log.trace('request days')
        menus = self.__menu_db.find_by_username(message_request.command_parts[2])
        days = []
        for menu in menus:
            day = menu.get('date', None)
            if day:
                days.append(day)

        inline_days = []
        for day in days:
            inline_days.append([{
                'text': day,
                'callback_data': f"{message_request.message_id} " + " ".join(message_request.command_parts) + ' ' + day}]
            )
        return MessageResponse(message_request.chat_id, 'Day:', json.dumps({
            'inline_keyboard': inline_days
        }), message_id = message_request.message_id)