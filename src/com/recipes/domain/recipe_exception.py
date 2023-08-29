class RecipeException(Exception):
    def __init__(self, message, statusCode):
        self.message = message
        self.statusCode = statusCode