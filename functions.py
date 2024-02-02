


def int_to_ascii(data):
    word = str(data)
    if len(word) == 3:
        result = word
    elif len(word) == 2:
        result = '0' + word
    elif len(word) == 1:
        result = '00' + word
    return result
