eng_alphabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k",
                "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v",
                "w", "x", "y", "z"]


def check_phone_format(checkstring: str):
    """
        Returns True, if phone from message complies with the standards, else False
    """
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
    """
        Returns True, if email from message complies with the standards, else False
    """
    is_dog_detected = False
    is_dot_detected = False  # переменная для обозначения наличия точки после наличия собаки
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


def _test():
    """
        Test function. Do not use in main program
    """
    command = input("Введите команду: ")
    if command == "phone":
        string = input("Введите любую строку, которая похожа на номер телефона: ")
        result = check_phone_format(string)
    elif command == "email":
        string = input("Введите любую строку, которая похожа на адрес электронной почты: ")
        result = check_email_format(string)
    elif command == "/exit":
        return 0
    else:
        return "Ты долбаёб?"
    return result


if __name__ == "__main__":
    test_result = _test()
    print(test_result)
