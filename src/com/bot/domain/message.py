class Message:
    def __init__(self, chat_id, text, reply_markup = None):
        self.__text = text
        self.__reply_markup = reply_markup
        self.__chat_id = chat_id
        self.__parse_mode = 'MarkdownV2'

    @property
    def chat_id(self):
        return self.__chat_id

    @property
    def text(self):
        return self.__text

    @property
    def payload(self):
        payload = {
            'parse_mode': self.__parse_mode,
            'chat_id': self.__chat_id,
            'text': self.__text
        }
        print(self.__reply_markup)
        if self.__reply_markup:
            payload['reply_markup'] = self.__reply_markup

        return payload