def handle_exception(e):
    return {"error":e.message},e.statusCode