import datetime
import json

import inject

from .format import escape_markdown_v2
from ..domain.message_request import MessageRequest
from ..domain.message_response import MessageResponse
from ...menus.domain.menu_database import MenuDatabase
from ...menus.domain.menu_exception import MenuException
from ...utils.log import Log


class Menu:
    @inject.autoparams()
    def __init__(self, log: Log, menu_db: MenuDatabase):
        self.__log = log
        self.__menu_db = menu_db
        self.__commands = {
            'get': self.get
        }

    def resolver(self, message_request: MessageRequest):
        self.__log.trace('Menu resolver {0}', message_request)
        return self.__commands[message_request.command_parts[1]](message_request)

    def get(self, message_request: MessageRequest):
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
        if isinstance(data['products'], dict):
            for comida, items in data['products'].items():
                mensaje += f"🍽️ *{escape_markdown_v2(comida)}:*\n"
                for item in items:
                    if 'recipe_name' in item and item['recipe_name']:
                        mensaje += f"   \- {escape_markdown_v2(item['name'])} \(Cantidad: {escape_markdown_v2(item['value'])} \- Receta: {escape_markdown_v2(item['recipe_name'])}\)\n"
                    else:
                        mensaje += f"   \- {escape_markdown_v2(item['name'])} \(Cantidad: {escape_markdown_v2(item['value'])}\)\n"

        return mensaje


    def get_week_days(self):
        hoy = datetime.datetime.now()

        monday = hoy - datetime.timedelta(days=hoy.weekday())

        week_days = []

        for i in range(7):
            day = monday + datetime.timedelta(days=i)
            week_days.append(day)

        return week_days

    def request_users(self, message_request: MessageRequest):
        return MessageResponse(message_request.chat_id, 'Choose user:', json.dumps({
            'inline_keyboard': [[
                {'text': 'Elias', 'callback_data': f'{message_request.message_id} /menu get elias'},
                {'text': 'Roma', 'callback_data': f'{message_request.message_id} /menu get roma'},
            ]]
        }), message_id = message_request.message_id)

    def request_days(self, message_request):
        week_days = self.get_week_days()
        inline_days = []
        for day in week_days:
            inline_days.append([{
                'text': day.strftime('%Y-%m-%d'),
                'callback_data': f"{message_request.message_id} " + " ".join(message_request.command_parts) + ' ' + day.strftime('%Y-%m-%d')}]
            )
        return MessageResponse(message_request.chat_id, 'Day:', json.dumps({
            'inline_keyboard': inline_days
        }), message_id = message_request.message_id)