import datetime
import json

import inject

from .format import escape_markdown_v2
from ..domain.message_request import MessageRequest
from ..domain.message_response import MessageResponse
from ...menus.domain.menu_database import MenuDatabase
from ...menus.domain.menu_exception import MenuException
from ...utils.log import Log
from ...weekly_menus.application.get_weekly_menu import GetWeeklyMenu
from ...weekly_menus.domain.weekly_menu_database import WeeklyMenuDatabase
from ...weekly_menus.domain.weekly_menu_exception import WeeklyMenuException


class WeeklyMenu:
    @inject.autoparams()
    def __init__(self, log: Log, get_weekly_menu: GetWeeklyMenu):
        self.__log = log
        self.__get_weekly_menu = get_weekly_menu
        self.__commands = {
            'get': self.get
        }

    def resolver(self, message_request: MessageRequest):
        self.__log.trace('WeeklyMenu resolver {0}', message_request)
        return self.__commands[message_request.command_parts[1]](message_request)

    def get(self, message_request: MessageRequest):
        if message_request.command_parts_length == 2:
            return self.request_users(message_request)

        if message_request.command_parts_length == 3:
            return self.request_weeks(message_request)

        try:
            return MessageResponse(message_request.chat_id, self.formatear(self.__get_weekly_menu.execute(message_request.command_parts[2], message_request.command_parts[3])), message_id = message_request.message_id)
        except WeeklyMenuException:
            date = message_request.command_parts[3].replace('-', '\-')
            return MessageResponse(message_request.chat_id, f'There are not a weekly_menu for {message_request.command_parts[2]} on {date}', message_id = message_request.message_id)

    def get_weeks(self):
        semanas = []
        hoy = datetime.datetime.now()

        # Obtener el lunes de esta semana
        lunes_actual = hoy - datetime.timedelta(days=hoy.weekday())

        # Iterar desde esta semana hasta las 3 anteriores
        for i in range(4):
            # Calcular el lunes y domingo de cada semana
            lunes = lunes_actual - datetime.timedelta(weeks=i)
            domingo = lunes + datetime.timedelta(days=6)

            # Obtener el número de la semana
            numero_semana = lunes.isocalendar()[1]

            # Formatear las fechas
            lunes_formateado = lunes.strftime('%m-%d')
            domingo_formateado = domingo.strftime('%m-%d')

            # Añadir a la lista el formato [número semana] mes-dia del lunes / mes-dia del domingo
            semanas.append({'number': lunes.strftime("%Y-W%W"), 'text': f"Del {lunes_formateado} al {domingo_formateado}"})

        return semanas

    def request_users(self, message_request: MessageRequest):
        return MessageResponse(message_request.chat_id, 'Choose user:', json.dumps({
            'inline_keyboard': [[
                {'text': 'Elias', 'callback_data': f'{message_request.message_id} /weekly-menu get elias'},
                {'text': 'Roma', 'callback_data': f'{message_request.message_id} /weekly-menu get roma'},
            ]]
        }), message_id = message_request.message_id)

    def request_weeks(self, message_request):
        weeks = self.get_weeks()
        inline_days = []
        for week in weeks:
            inline_days.append([{
                'text': week['text'],
                'callback_data': f"{message_request.message_id} " + " ".join(message_request.command_parts) + f" {week['number']}"}]
            )
        return MessageResponse(message_request.chat_id, 'Day:', json.dumps({
            'inline_keyboard': inline_days
        }), message_id = message_request.message_id)

    def formatear(self, data):
        # Escapando el nombre del usuario
        username = escape_markdown_v2(data.get('username', 'Desconocido'))

        # Escapando el número de la semana
        weekly_number = escape_markdown_v2(data.get('weekly_number', 'No especificado'))

        mensaje = f"*Usuario:* {username}\n*Número de semana:* {weekly_number}\n\n"

        for fecha, detalles in data.get('menus', {}).items():
            mensaje += f"*Fecha:* {escape_markdown_v2(fecha)}\n\n"

            # Valores nutricionales
            mensaje += "*Valores Nutricionales:*\n"
            for valor in detalles.get('nutritional_value', []):
                nombre = escape_markdown_v2(valor['name'])
                cantidad = escape_markdown_v2(str(valor['value']))
                unidad = escape_markdown_v2(valor['unit'])
                mensaje += f" \- {nombre}: {cantidad} {unidad}\n"

            # Recetas
            mensaje += "\n*Recetas:*\n"
            for receta in detalles.get('recipes', []):
                mensaje += f" \- {escape_markdown_v2(receta)}\n"

            # Productos
            mensaje += "\n*Productos:*\n"
            for producto in detalles.get('products', []):
                nombre_producto = escape_markdown_v2(producto['name'])
                cantidad_producto = escape_markdown_v2(str(producto['value']))
                mensaje += f" \- {nombre_producto} \(Cantidad: {cantidad_producto}\)\n"

            mensaje += "\n"

        return mensaje