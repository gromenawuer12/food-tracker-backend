def escape_markdown_v2(text):
    if text is not None:
        char_to_scape = ['_', '*', '[', ']', '(', ')', '~', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']
        char_scaped = ['\_', '\*', '\[', '\]', '\(', '\)', '\~', '\>', '\#', '\+', '\-', '\=', '\|', '\{', '\}', '\.', '\!']
        for index, char in enumerate(char_to_scape):
            text = text.replace(char, char_scaped[index])
    return text