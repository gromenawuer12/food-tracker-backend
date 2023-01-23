import re, json

from .users.infrastructure.api.users_blueprint import UsersBlueprint


def users_blueprint(event):
    usersBlueprint = UsersBlueprint()
    # check httpMethod y mejorar
    if re.search('/users/login', event['path']):
        return usersBlueprint.login(event['headers'])
    return eval({
                    'GET': "usersBlueprint.get()",
                    'POST': "usersBlueprint.post(event['body'])",
                    'PUT': "usersBlueprint.modify()"
                }[event['httpMethod']])


def resolve(paths, event):
    for key in paths:
        if re.search(key, event['path']):
            # print(event['httpMethod'])
            # usar eval() ???
            return eval(paths[key])(event)
