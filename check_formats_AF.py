eng_alphabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k",
                "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v",
                "w", "x", "y", "z"]
rus_alphabet = ["а", "б", "в", "г", "д", "е", "ё", "ж", "з", "и", "й",
                "к", "л", "м", "н", "о", "п", "р", "с", "т", "у", "ф",
                "х", "ц", "ч", "ш", "щ", "ъ", "ы", "ь", "э", "ю", "я"]


def check_phone_format(checkstring: str):
    for symbol in checkstring:
        if not symbol.isdigit():
            return "error"
    try:
        result = int(checkstring)
    except ValueError:
        return "error"
    return result


def check_email_format(checkstring: str):
    is_dog_detected = False
    is_all_right = False
    for symbol in checkstring:
        if symbol in eng_alphabet or symbol.lower() in eng_alphabet or symbol == ".":
            is_all_right = True
        elif symbol == "@":
            is_dog_detected = True
    if is_all_right and is_dog_detected:
        return checkstring
    else:
        return "error"


def check_address_format(checkstring: str):
    for symbol in checkstring:
        if (symbol not in rus_alphabet or symbol.lower not in rus_alphabet) and symbol != ",":
            return "error"
    return checkstring
