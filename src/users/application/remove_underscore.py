import sys, re
from ..domain.user import User
from functools import wraps


def remove_underscore(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        user = vars(f(*args, **kwargs))
        for key in list(user.keys()):
            if re.search(r"_.*", key):
                new_key = key.replace("_", "")
                user[new_key] = user[key]
                del user[key]

        return user

    return decorator
