eng_alphabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k",
                "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v",
                "w", "x", "y", "z"]
rus_small_alphabet = ["а", "б", "в", "г", "д", "е", "ё", "ж", "з", "и", "й",
                      "к", "л", "м", "н", "о", "п", "р", "с", "т", "у", "ф",
                      "х", "ц", "ч", "ш", "щ", "ъ", "ы", "ь", "э", "ю", "я"]
rus_big_alphabet = ["А", "Б", "В", "Г", "Д", "Е", "Ё", "Ж", "З", "И", "Й",
                    "К", "Л", "М", "Н", "О", "П", "Р", "С", "Т", "У", "Ф",
                    "Х", "Ц", "Ч", "Ш", "Щ", "Ъ", "Ы", "Ь", "Э", "Ю", "Я"]


def check_phone_format(checkstring: str):
    is_plus = False
    for symbol in checkstring:
        if symbol == "+" and checkstring.index(symbol) == 0:
            if not is_plus:
                is_plus = True
            else:
                return "error"
        if symbol.isdigit():
            pass
        if (is_plus and checkstring.__sizeof__() != 61) or (not is_plus and checkstring.__sizeof__() != 60):
            return "error"
        else:
            return checkstring


def check_email_format(checkstring: str):
    is_dog_detected = False
    is_dot_detected = False  # переменная для обозначения наличия точки после собаки
    is_all_right = False
    for symbol in checkstring:
        if symbol in eng_alphabet or \
                symbol.lower() in eng_alphabet or \
                symbol == ".":
            is_all_right = True
        elif symbol == "@":
            is_dog_detected = True
        else:
            is_all_right = False
        if symbol == "." and is_dog_detected:
            is_dot_detected = True
        if not is_all_right:
            break
    if is_all_right and is_dog_detected and is_dot_detected:
        return checkstring
    else:
        return "error"


def check_address_format(checkstring: str):
    for symbol in checkstring:
        if symbol in rus_small_alphabet or symbol in rus_big_alphabet or symbol.isdigit() or \
                symbol == "," or symbol == "." or symbol == " ":
            continue
        return "error"
    return checkstring


def test():
    command = input("Введите команду: ")
    if command == "phone":
        string = input("Введите любую строку, которая похожа на номер телефона: ")
        result = check_phone_format(string)
    elif command == "email":
        string = input("Введите любую строку, которая похожа на адрес электронной почты: ")
        result = check_email_format(string)
    elif command == "address":
        string = input("Введите любую строку, которая похожа на адрес, в котором живёт человек: ")
        result = check_address_format(string)
    elif command == "/exit":
        return 0
    else:
        return "Ты долбаёб?"
    return result


if __name__ == "__main__":
    test_result = test()
    print(test_result)
    # com = input("s: ")
    # print(com.__sizeof__())
