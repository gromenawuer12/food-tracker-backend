from functools import wraps

import jwt
import os

from .token_invalid_exception import TokenInvalidException


def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        if 'headers' not in kwargs['event'] or 'Authorization' not in kwargs['event']['headers']:
            print('Error getting token')
            raise TokenInvalidException()
        token = kwargs['event']['headers']['Authorization'].split()[1]
        try:
            payload = jwt.decode(token, os.getenv('SECRET_KEY'), algorithms=["HS256"])
            kwargs['event']['auth_username'] = payload['username']
        except jwt.exceptions.ExpiredSignatureError:
            raise jwt.exceptions.ExpiredSignatureError()
        except Exception:
            print('Error getting token')
            raise TokenInvalidException()

        return f(*args, **kwargs)

    return decorator
