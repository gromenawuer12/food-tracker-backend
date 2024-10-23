import datetime
import json

import inject

from ..domain.message import Message
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

    def resolver(self, chat_id, command):
        command_parts = command.split()
        self.__log.trace('Menu resolver {0} {1}', chat_id, command_parts)
        return self.__commands[command_parts[1]](chat_id, command_parts)

    def get(self, chat_id, command_parts):
        command_parts_length = len(command_parts)
        if command_parts_length == 2:
            return Message(chat_id, 'Choose user:', json.dumps({
                'inline_keyboard': [[
                    {'text': 'Elias', 'callback_data': '/menu get elias'},
                    {'text': 'Roma', 'callback_data': '/menu get roma'},
                ]]
            }))

        if command_parts_length == 3:
            week_days = self.get_week_days()
            inline_days = []
            for day in week_days:
                inline_days.append({
                    'text': day,
                    'callback_data': " ".join(command_parts) + ' ' + day}
                )
            return Message(chat_id, 'Day:', json.dumps({
                'inline_keyboard': [inline_days]
            }))

        try:
            return Message(chat_id, self.format(self.__menu_db.find(command_parts[2], command_parts[3])))
        except MenuException:
            date = command_parts[3].replace('-', '\-')
            return Message(chat_id, f'There are not a menu for {command_parts[2]} on {date}')

    def today(self):
        return self.format(self.__menu_db.find('elias', datetime.date.today().strftime("%Y-%m-%d")))

    def escape_markdown_v2(self, text):
        self.__log.trace('escape_markdown_v2 {0}', text)
        char_to_scape = ['_', '*', '[', ']', '(', ')', '~', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']
        char_scaped = ['\_', '\*', '\[', '\]', '\(', '\)', '\~', '\>', '\#', '\+', '\-', '\=', '\|', '\{', '\}', '\.', '\!']
        for index, char in enumerate(char_to_scape):
            text = text.replace(char, char_scaped[index])
        return text

    def format(self, data):
        self.__log.trace('format {0}', data)
        mensaje = f"📅 *Fecha:* {self.escape_markdown_v2(data['date'])}\n"
        mensaje += f"👤 *Usuario:* {self.escape_markdown_v2(data['username'])}\n\n"
        mensaje += "*Valores Nutricionales:*\n"
        for item in data['nutritional_value']:
            mensaje += f" \- {self.escape_markdown_v2(item['name'])}: {self.escape_markdown_v2(item['value'])} {self.escape_markdown_v2(item['unit'])}\n"

        mensaje += "\n*Productos:*\n"
        for comida, items in data['products'].items():
            mensaje += f"🍽️ *{self.escape_markdown_v2(comida)}:*\n"
            for item in items:
                if 'recipe_name' in item and item['recipe_name']:
                    mensaje += f"   \- {self.escape_markdown_v2(item['name'])} (Cantidad: {self.escape_markdown_v2(item['value'])} \- Receta: {self.escape_markdown_v2(item['recipe_name'])})\n"
                else:
                    mensaje += f"   \- {self.escape_markdown_v2(item['name'])} (Cantidad: {self.escape_markdown_v2(item['value'])})\n"

        return mensaje


    def get_week_days(self):
        hoy = datetime.datetime.now()

        monday = hoy - datetime.timedelta(days=hoy.weekday())

        week_days = []

        for i in range(7):
            day = monday + datetime.timedelta(days=i)
            week_days.append(day.strftime('%Y-%m-%d'))

        return week_days