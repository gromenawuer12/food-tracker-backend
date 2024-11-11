import json

import inject

from .format import escape_markdown_v2
from ..domain.message_request import MessageRequest
from ..domain.message_response import MessageResponse
from ...recipes.application.get_recipe import GetRecipe
from ...utils.log import Log


class Recipe:
    @inject.autoparams()
    def __init__(self, log: Log, get_recipe: GetRecipe):
        self.__log = log
        self.__get_recipe = get_recipe
        self.__commands = {
            'help': self.__help,
            'get': self.__get,
            'search': self.__search
        }

    def resolver(self, message_request: MessageRequest):
        self.__log.trace('Recipe resolver {0}', message_request.to_string())
        return self.__commands[message_request.command_parts[1]](message_request)

    def __help(self, message_request: MessageRequest):
        return MessageResponse(message_request.chat_id, '`/recipes get <THE+NAME>`\n`/recipes search <TEXT>`', message_id = message_request.message_id)

    def __search(self, message_request: MessageRequest):
        if message_request.command_parts_length == 3:
            recipes = self.__get_recipe.execute(None, message_request.command_parts[2])

            if len(recipes['items']) == 0:
                return MessageResponse(message_request.chat_id, f'There are not recipes that contains "{message_request.command_parts[2]}"', message_id = message_request.message_id)

            inline_recipes = []
            for recipe in recipes['items'][:5]:
                name = recipe['name']
                inline_recipes.append([{
                    'text': name,
                    'callback_data': f"{message_request.message_id} " + " /recipes get " + "+".join(name.split())}]
                )
            return MessageResponse(message_request.chat_id, 'Recipes:', json.dumps({
                'inline_keyboard': inline_recipes
            }), message_id = message_request.message_id)

        return MessageResponse(message_request.chat_id, f'Only search is needed', message_id = message_request.message_id)

    def __get(self, message_request: MessageRequest):
        if message_request.command_parts_length == 3:
            recipe = self.__get_recipe.execute(' '.join(message_request.command_parts[2].split('+')))
            self.__log.trace(recipe)
            return MessageResponse(message_request.chat_id, self.__format(recipe), message_id = message_request.message_id)

        return MessageResponse(message_request.chat_id, f'Only name is needed', message_id = message_request.message_id)

    def __format(self, data):
        self.__log.trace('format {0}', data)
        output = f"*Recipe*: {data['name']}\n\n"
        self.__log.trace('format {0}', output)

        output += "*Nutritional Value*:\n"
        for nutrient in data['nutritional_value']:
            name = escape_markdown_v2(nutrient['name'])
            value = escape_markdown_v2(nutrient['value'])
            unit = escape_markdown_v2(nutrient['unit'])
            output += f"\- *{name}*: {value} {unit}\n"
        self.__log.trace('format {0}', output)

        output += "\n*Ingredientes*:\n"
        for product in data['products']:
            ingredient = escape_markdown_v2(product[0])
            unit = escape_markdown_v2(product[1])
            quantity = escape_markdown_v2(product[2])
            output += f"\- {ingredient}: {quantity} {unit}\n"
        self.__log.trace('format {0}', output)

        if data['description']:
            output += "\n*Instructions:*\n"
            output += data['description'].replace('.', '\.')
        self.__log.trace('format {0}', output)

        return output