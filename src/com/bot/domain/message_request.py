class MessageRequest:
    def __init__(self, chat_id, command):
        self.__command = command
        self.__chat_id = chat_id
        command_parts = command.split()
        self.__message_id =  command_parts[0] if '/' not in command_parts[0] else None
        self.__command_parts = command_parts[1:] if self.__message_id else command_parts
        self.__command_parts_length = len(self.__command_parts)

    @property
    def command(self):
        return self.__command

    @property
    def command_parts(self):
        return self.__command_parts

    @property
    def command_parts_length(self):
        return self.__command_parts_length

    @property
    def chat_id(self):
        return self.__chat_id

    @property
    def message_id(self):
        return self.__message_id

    def to_string(self):
        return f'{{"chat_id": {self.__chat_id}, "mesage_id": {self.__message_id}, "command_parts": {self.__command_parts}}}'