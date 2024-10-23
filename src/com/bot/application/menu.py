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
            return Message(chat_id, f'There are not a menu for {command_parts[2]} on {command_parts[3]}')

    def today(self):
        return self.format(self.__menu_db.find('elias', datetime.date.today().strftime("%Y-%m-%d")))

    def format(self, data):
        self.__log.trace(data)
        date = data['date'].replace('-', '\-')
        nutritional_values = data['nutritional_value']
        recipes = ", ".join(data['recipes'])
        products = "\n".join([f"{item['name']}: {item['value']}" for item in data['products']])

        # Formatear el mensaje
        message = f"\n__Menu de: {data['username']}__\n\n"
        message += f"*Fecha:* {date}\n\n"
        message += "*Valor Nutricional:*\n"

        for item in nutritional_values:
            value = item['value'].replace('.', '\.')
            message += f"{item['name']}: {value} {item['unit']}\n"

        message += f"\n*Recetas:* {recipes}\n"
        message += f"\n*Productos:*\n{products}\n"

        return message

    def get_week_days(self):
        hoy = datetime.datetime.now()

        monday = hoy - datetime.timedelta(days=hoy.weekday())

        week_days = []

        for i in range(7):
            day = monday + datetime.timedelta(days=i)
            week_days.append(day.strftime('%Y-%m-%d'))

        return week_days