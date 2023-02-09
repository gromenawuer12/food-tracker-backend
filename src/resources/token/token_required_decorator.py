import jwt, os, sys
from functools import wraps
from .token_invalid_exception import TokenInvalidException


def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):

        if not 'Authorization' in kwargs['headers']:
            raise TokenInvalidException()
        token = kwargs['headers']['Authorization'].split()[1]
        try:
            payload = jwt.decode(token, os.getenv('SECRET_KEY'), algorithms=["HS256"])
            kwargs['auth_username'] = payload['username']
        except:
            raise TokenInvalidException()

        return f(*args, **kwargs)

    return decorator
