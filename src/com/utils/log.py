import os

log_levels = {
    'TRACE': 0,
    'DEBUG': 1,
    'INFO': 2,
    'ERROR': 3
}


class Log:
    def __init__(self, request_id):
        self.requestId = request_id
        self.level = log_levels.get(os.getenv('LOG_LEVEL'))

    def debug(self, text: str, *args):
        self.__print('DEBUG', text, *args)

    def trace(self, text: str, *args):
        self.__print('TRACE', text, *args)

    def error(self, text: str, *args):
        self.__print('ERROR', text, *args)

    def __print(self, level, text: str, *args):
        if self.level <= log_levels.get(level):
            if len(args) != 0:
                print(self.requestId + ': ', level, ' -> ', text.format(*args))
            else:
                print(self.requestId + ': ', level, ' -> ', text)
