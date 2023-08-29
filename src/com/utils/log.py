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

    def debug(self, text):
        self.__print('DEBUG', text)

    def trace(self, text):
        self.__print('TRACE', text)

    def error(self, text):
        self.__print('ERROR', text)

    def __print(self, level, text):
        if self.level <= log_levels.get(level):
            print(self.requestId + ': ', level, ' -> ', text)
