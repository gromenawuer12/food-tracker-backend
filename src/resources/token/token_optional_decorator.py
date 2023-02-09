import jwt, os, sys
from functools import wraps
from .token_invalid_exception import TokenInvalidException


def token_optional(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        if 'Authorization' in kwargs['headers'] and kwargs['headers']['Authorization'].split()[0] == 'Bearer':
            token = kwargs['headers']['Authorization'].split()[1]
            try:
                payload = jwt.decode(token, os.getenv('SECRET_KEY'), algorithms=["HS256"])
                kwargs['auth_username'] = payload['username']
            except:
                raise TokenInvalidException()
        return f(*args, **kwargs)

    return decorator
