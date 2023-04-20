"""
    Как добавить какой-либо этап в код, не поломав при этом ничего? Всё очень просто!
    Т.к. поэтапная система завязана на переменной current_stage, то мы просто следуем за этими шагами:
        1. Придумайте название этапа такое, чтобы оно отображало суть Вашего вопроса. Нам нужна читабельность кода,
        поэтому нужно использовать 1 слово. Если не получилось, то можно использовать 2-3 слова, не больше
        (обычно используется в случаях, когда сам этап предполагает ответвления -
        разные действия под одинаковым предлогом);
        2. Придумайте текст, который Вы собираетесь выводить на этом этапе;
        3. Продумайте логику, которая будет исполняться ПОСЛЕ того, как пользователь отправит "ответ" на Ваш "вопрос";
        4. Добавьте текст состояния из шага 2 в переменную current_stage_list. Главное, не забудьте, в каком месте
        в списке Вы его поместили;
        Теперь, когда мы знаем, что именно мы хотим добавить в этап, мы идём дальше, а именно к самому коду:
            Если мы собираемся создавать этап в конце всей программы, то:
                5. Пишем в конце блока с условием последнего этапа то,
                что мы хотим написать пользователю (текст из шага 2);
                6. Пишем в конце функции условие elif current_stage == "current_stage_list[индекс состояния в списке]":
                (или конструкцию else, если по логике этапа необходимо исключающее условие,
                но никак не if, потому что он сломает всю целостность структуры и будет "лететь вперёд паровоза",
                т.е. собьётся порядок);
                7. В блоке условия из шага 6 мы пишем логику из шага 3 и переход на нулевой
                этап (current_stage = "None").
            Если мы собираемся создавать этап между двумя существующими ("один" и "два"), то:
                (здесь алгоритм чуть сложнее объяснить, но суть алгоритма та же)
                5. В конце кода этапа "один" мы прописываем то, что мы хотим написать пользователю (текст из шага 2);
                6. Между этапом "один" и "два" прописываем условие
                elif current_stage == "current_stage_list[индекс состояния в списке]":
                (никак не if, потому что он сломает всю целостность структуры и будет "лететь вперёд паровоза",
                т.е. собьётся порядок);
                7. В блоке условия из шага 6 мы пишем логику из шага 3.
    Как видите, ничего сложного нет! Надо только понимать логику прохождения программы по этапам.
"""

import telebot
from telebot import types

from config import abit_sfedu_bot
from check_formats_AF import check_phone_format, check_email_format, check_address_format
from about_func_AF import about_func
from sql_AF import get_info_from_abiturient, get_info_about_message, clear_table

bot = telebot.TeleBot(abit_sfedu_bot)
markup_remove = types.ReplyKeyboardRemove()
current_stage = "None"
debug_stage = 0
is_force_exit = False
is_phone_defined = False
is_address_defined = False
is_email_defined = False
is_debug = False
is_finished = False
abit_data: dict = {
    "name": "",
    "surname": "",
    "patronymic": "",
    "phone": 0,
    "email": "",
    "address": "",
    "school": "",
    "class": "",
    "city": ""
}
variables_list = {
    "p_d": types.KeyboardButton("is_phone_defined"),  # , callback_data="p_d"
    "e_d": types.KeyboardButton("is_email_defined"),  # , callback_data="e_d"
    "a_d": types.KeyboardButton("is_address_defined"),  # , callback_data="a_d"
    "message_list": ...,
    "markup_choice": types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
}
message_counter = 0
variables_list["markup_choice"].add(variables_list["p_d"], variables_list["e_d"], variables_list["a_d"])
is_admin_choice = False
is_blocked = False


def manager(message):
    get_info_about_message(message.chat.id, message.text)
    if message.text == "/about":
        about(message)
    elif message.text == "/!admin":
        non_admin(message)
    elif message.text == "/admin" or debug_stage > 0:
        admin(message)
    elif current_stage == "None" and message.text == "/start":
        start(message)
    elif current_stage in ["Старт", "Инициалы", "Город", "Школа", "Класс",
                           "Контактные данные: опрос", "Контактные данные: ввод"]:
        agree(message)

    elif current_stage not in ["None", "Старт", "Инициалы", "Город", "Школа", "Класс",
                               "Контактные данные: опрос", "Контактные данные: ввод"]:
        bot.send_message(message.chat.id, "<b>Извините, возникли неполадки в программе. "
                                          "Выполняю принудительное завершение работы...</b>", parse_mode='html')
        bot.stop_bot()
        raise SystemError("Сбой в программе! Неправильное название этапа!")

    return is_finished


def about(message):
    global markup_remove
    about_func(message, bot, markup_remove)


def admin(message):
    global debug_stage, is_debug, is_phone_defined, is_email_defined, is_address_defined, is_admin_choice, is_blocked
    if current_stage == "Инициалы" or current_stage == "Контактные данные: ввод":
        bot.send_message(message.chat.id, "Не знаю почему, но на данном этапе программы команда /!admin не возвращает "
                                          "на исходное положение. Причём на остальных этапах всё работает нормально. "
                                          "В этом, правда, виноваты условия, но я не знаю, как обойти этот баг... "
                                          "Поэтому здесь просто заглушка, не дающая войти в режим разработчика.\n"
                                          "К превеликому сожалению, на данном этапе нельзя использовать "
                                          "команду /admin... Просто смиритесь с этим)")
    elif not is_debug:
        text = ""
        if debug_stage == 0:
            bot.send_message(message.chat.id, "Ты разработчик? Докажи!")
            text = "<b>Первый вопрос:</b> как называется этот проект?"
            bot.send_message(message.chat.id, text, parse_mode='html')

            debug_stage += 1
        elif debug_stage == 1:
            if message.text == "Abiturient's folder":
                text = "Хорошо, <b>второй вопрос</b>: какой самый первый язык программирования изучал разработчик?"
                debug_stage += 1
            else:
                if message.text == "Сбор данных об абитуриентах":
                    text = "Хорошая попытка, умник, <b>но нет</b>. Ты не разработчик."
                elif message.text == "@abit_sfedu_bot":
                    text = "*саркастично хлопает* Молодец. Но ты не разработчик."
                else:
                    text = "Не-а, даже не близко. Ты не разработчик."
                is_debug = False
                debug_stage = 0

            bot.send_message(message.chat.id, text, parse_mode='html')
        elif debug_stage == 2:
            if message.text == "HtML":
                text = "Итак, теперь <b>третий вопрос</b>, да не простой, а на засыпку: сколько раз разработчик " \
                       "пробовал писать ботов, прежде чем он \"нашёл\" свой стиль?"
                debug_stage += 1
            else:
                if message.text == "html" or message.text == "HTML":
                    text = "Ха! Я тебя подловил! Даже если ты знал ответ на этот вопрос, " \
                           "то этот ответ явно не засчитывается. Ты не разработчик."
                else:
                    text = "Не-а, даже не близко. Ты не разработчик."
                is_debug = False
                debug_stage = 0

            bot.send_message(message.chat.id, text, parse_mode='html')
        elif debug_stage == 3:
            if message.text == "11":
                text = "Теперь я верю тебе. Ты разработчик."
                debug_stage += 2
                is_debug = True
            else:
                text = "Не-а, даже не близко. Ты не разработчик."
                is_debug = False
                debug_stage = 0

            bot.send_message(message.chat.id, text, parse_mode='html')
            if is_debug:
                text = "Можно очистить данные из обоих таблиц командами /delst и /delse (ты знаешь, " \
                       "за что они отвечают, поэтому будь осторожен). Если что, выйти из режима разработчика " \
                       "можно командой /!admin. По остальным командам пиши /ahelp"
                if not current_stage.startswith("Контактные данные"):
                    global is_phone_defined, is_email_defined, is_address_defined
                    variables_list["message_list"] = \
                        bot.send_message(message.chat.id,
                                         "Эти переменные можно изменить:\n\n"
                                         f"     is_phone_defined: {is_phone_defined}\n"
                                         f"     is_email_defined: {is_email_defined}\n"
                                         f"     is_address_defined: {is_address_defined}\n"
                                         "\nВ меню кнопок выбирай переменную, значение которой хочешь "
                                         "поменять на противоположное.\n"
                                         f"{text}",
                                         reply_markup=variables_list["markup_choice"])
                else:
                    bot.send_message(message.chat.id, f"На данном этапе бесполезно менять те три переменные,"
                                                      f" поэтому они отключены. {text}", reply_markup=markup_remove)
                    is_blocked = True
    else:
        if message.text.startswith("/del"):
            import sqlite3
            try:
                if message.text.endswith("st"):
                    clear_table("students")
                elif message.text.endswith("se"):
                    clear_table("sent_messages")
            except sqlite3.DatabaseError as e:
                result = "с ошибкой!"
                print(e)
            else:
                result = "успешно!"
            text = "Очистка данных таблицы проведена <b>" + result + "</b>"
            bot.send_message(message.chat.id, text, parse_mode='html')
        elif message.text == "/clch":
            is_phone_defined = False
            is_email_defined = False
            is_address_defined = False
            is_admin_choice = False
            bot.send_message(message.chat.id, "Все изменения были отменены!")
        elif message.text == "/ahelp":
            bot.send_message(message.chat.id, "Доступные команды:\n\n\n"
                                              "    <u>/ahelp</u> - admin help - показывает список команд, доступных "
                                              "ТОЛЬКО в режиме разработчика;\n\n"
                                              "    <u>/clch</u> - clear changes - отменяет изменения "
                                              "значений трёх переменных, сделанные разработчиком;\n\n"
                                              "    <u>/delst</u> - delete students - очищает таблицу students в БД;\n\n"
                                              "    <u>/delse</u> - delete sent(_messages) - очищает таблицу "
                                              "sent_messages в БД;\n\n"
                                              "    <u>/!admin</u> - not admin - выход из режима разработчика "
                                              "с возвращением на тот этап программы/сценария, на котором была вызвана "
                                              "команда /admin.\n\n\n"
                                              "Будьте осторожны! <b>Нерациональное изменение параметров может "
                                              "повлиять на работу всего сценария!</b>",
                             parse_mode='html')
        elif message.text == "/admin":
            bot.send_message(message.chat.id, "Вы <b>уже</b> находитесь в режиме разработчика!", parse_mode='html')
        else:
            if not is_blocked:
                if message.text == "is_phone_defined":
                    is_phone_defined = True if not is_phone_defined else False
                elif message.text == "is_email_defined":
                    is_email_defined = True if not is_email_defined else False
                elif message.text == "is_address_defined":
                    is_address_defined = True if not is_address_defined else False
                bot.send_message(message.chat.id, "Эти переменные можно изменить:\n"
                                                  f"     is_phone_defined: {is_phone_defined}\n"
                                                  f"     is_email_defined: {is_email_defined}\n"
                                                  f"     is_address_defined: {is_address_defined}\n",
                                 reply_markup=variables_list["markup_choice"])
                is_admin_choice = True
            else:
                bot.send_message(message.chat.id, "Эти переменные заблокированы для изменений!")


def non_admin(message):
    global debug_stage, is_debug, current_stage
    debug_stage = 0
    is_debug = False
    bot.send_message(message.chat.id, "Вы вышли из режима разработчика!")
    message.text = ""
    get_prev_current_stage()
    start(message) if current_stage == "None" else agree(message)


def get_prev_current_stage():
    global current_stage
    if current_stage == "Старт":
        current_stage = "None"
    elif current_stage == "Инициалы":
        current_stage = "Старт"
    elif current_stage == "Город":
        current_stage = "Инициалы"
    elif current_stage == "Школа":
        current_stage = "Город"
    elif current_stage == "Класс":
        current_stage = "Школа"
    elif current_stage == "Контактные данные: опрос":
        current_stage = "Класс"
    elif current_stage == "Контактные данные: ввод":
        current_stage = "Контактные данные: опрос"


def set_text(user_id, check_text: str = ""):
    global is_phone_defined, is_email_defined, is_address_defined
    list_of_texts = ["апиши, пожалуйста, свой рабочий номер телефона, чтобы мы всегда могли тебе позвонить "
                     "и спросить, как у тебя дела :)",
                     "апиши, пожалуйста, свою рабочую электронную почту, чтобы мы всегда могли "
                     "написать тебе и спросить, как дела с долгами :)",
                     "апиши, пожалуйста, свой адрес, где ты прямо сейчас прописан(а), чтобы мы "
                     "могли найти тебя и к тебе в случае чего придёт военком :)",
                     "апиши, пожалуйста, телефон и электронную почту отдельными сообщениями, "
                     "чтобы бот смог различить данные",
                     "апиши, пожалуйста, адрес проживания и электронную почту отдельными сообщениями, "
                     "чтобы бот смог различить данные",
                     "апиши, пожалуйста, телефон и адрес проживания отдельными сообщениями, "
                     "чтобы бот смог различить данные",
                     "апиши, пожалуйста, телефон, электронную почту и адрес проживания отдельными сообщениями, "
                     "чтобы бот смог различить данные"
                     ]
    is_phone_defined = True \
        if not is_admin_choice and (check_text == "Телефон" or
                                    check_text == "И телефон, и email" or
                                    check_text == "И телефон, и адрес" or
                                    check_text == "Всё сразу") \
        else (True if is_admin_choice and is_phone_defined else False)
    is_email_defined = True \
        if not is_admin_choice and (check_text == "Email" or
                                    check_text == "И адрес, и email" or
                                    check_text == "И телефон, и email" or
                                    check_text == "Всё сразу") \
        else (True if is_admin_choice and is_email_defined else False)
    is_address_defined = True \
        if not is_admin_choice and (check_text == "Адрес проживания" or
                                    check_text == "И адрес, и email" or
                                    check_text == "И телефон, и адрес" or
                                    check_text == "Всё сразу") \
        else (True if is_admin_choice and is_address_defined else False)
    if check_text == "Телефон" or \
            (is_admin_choice and (is_phone_defined and not is_email_defined and not is_address_defined)):
        text = ("Тогда н" if not is_admin_choice else "Н") + list_of_texts[0]
    elif check_text == "Email" or \
            (is_admin_choice and (not is_phone_defined and is_email_defined and not is_address_defined)):
        text = ("Тогда н" if not is_admin_choice else "Н") + list_of_texts[1]
    elif check_text == "Адрес проживания" or \
            (is_admin_choice and (not is_phone_defined and not is_email_defined and is_address_defined)):
        text = ("Тогда н" if not is_admin_choice else "Н") + list_of_texts[2]
    elif check_text == "И телефон, и email" or \
            (is_admin_choice and (is_phone_defined and is_email_defined and not is_address_defined)):
        text = ("Тогда н" if not is_admin_choice else "Н") + list_of_texts[3]
    elif check_text == "И адрес, и email" or \
            (is_admin_choice and (not is_phone_defined and is_email_defined and is_address_defined)):
        text = ("Тогда н" if not is_admin_choice else "Н") + list_of_texts[4]
    elif check_text == "И телефон, и адрес" or \
            (is_admin_choice and (is_phone_defined and not is_email_defined and is_address_defined)):
        text = ("Тогда н" if not is_admin_choice else "Н") + list_of_texts[5]
    elif check_text == "Всё сразу" or \
            (is_admin_choice and (is_phone_defined and is_email_defined and is_address_defined)):
        text = ("Ого! Ты решил(а) всё сразу нам сказать? "
                "Какой(ая) ты молодец!\nВ таком случае н" if not is_admin_choice else "Н") + list_of_texts[6]
    else:
        bot.send_message(user_id, "<b>Извините, возникли неполадки в программе. "
                                  "Выполняю принудительное завершение работы...</b>", parse_mode='html')
        bot.stop_bot()
        raise SystemError("Сбой в программе! Ошибка в присвоении переменных!")
    return text


def fill_fields(check_text: str):
    global message_counter
    number_of_messages = 0
    if (is_phone_defined and not is_email_defined and not is_address_defined) or \
            (not is_phone_defined and is_email_defined and not is_address_defined) or \
            (not is_phone_defined and not is_email_defined and is_address_defined):
        number_of_messages = 1
    elif is_phone_defined and is_email_defined and is_address_defined:
        number_of_messages = 3
    elif (is_phone_defined and is_email_defined) or \
            (is_address_defined and is_email_defined) or \
            (is_phone_defined and is_address_defined):
        number_of_messages = 2
    message_counter += 1
    temp_phone = ""
    temp_email = ""
    temp_address = ""
    if message_counter == 1:
        if is_phone_defined:
            abit_data["phone"] = check_phone_format(check_text)
        if is_email_defined:
            abit_data["email"] = check_email_format(check_text)
        if is_address_defined:
            abit_data["address"] = check_address_format(check_text)
    elif message_counter == 2:
        if is_phone_defined and is_email_defined:
            temp_phone = check_phone_format(check_text)
            temp_email = check_email_format(check_text)
            if temp_phone == "error" and temp_email == "error":
                temp_phone, temp_email = temp_email, temp_phone
        elif is_address_defined and is_email_defined:
            temp_address = check_address_format(check_text)
            temp_email = check_email_format(check_text)
            if temp_address == "error" and temp_email == "error":
                temp_address, temp_email = temp_email, temp_address
        elif is_phone_defined and is_address_defined:
            temp_phone = check_phone_format(check_text)
            temp_address = check_address_format(check_text)
            if temp_phone == "error" and temp_address == "error":
                temp_phone, temp_address = temp_address, temp_phone
    elif message_counter == 3:
        temp_phone = check_phone_format(check_text)
        temp_email = check_email_format(check_text)
        temp_address = check_address_format(check_text)
        if temp_phone == "error" and temp_email == "error":
            temp_phone, temp_email = temp_email, temp_phone
        elif temp_address == "error" and temp_email == "error":
            temp_address, temp_email = temp_email, temp_address
        elif temp_phone == "error" and temp_address == "error":
            temp_phone, temp_address = temp_address, temp_phone
    abit_data["phone"] = temp_phone if temp_phone != "error" and \
        message_counter > 1 else "error"
    abit_data["email"] = temp_email if temp_email != "error" and \
        message_counter > 1 else "error"
    abit_data["address"] = temp_address if temp_address != "error" and \
        message_counter > 1 else "error"
    return True if message_counter == number_of_messages else False


def finish_session(message):
    global current_stage, is_phone_defined, \
        is_email_defined, is_address_defined, \
        is_debug, debug_stage, abit_data, is_force_exit
    get_info_from_abiturient(message.chat.id, abit_data["name"], abit_data["surname"],
                             abit_data["patronymic"], abit_data["phone"], abit_data["email"],
                             abit_data["address"], abit_data["school"], abit_data["class"],
                             abit_data["city"]) if not is_force_exit else ...
    current_stage = "None"
    abit_data["name"] = ""
    abit_data["surname"] = ""
    abit_data["patronymic"] = ""
    abit_data["phone"] = 0
    abit_data["email"] = ""
    abit_data["address"] = ""
    abit_data["school"] = ""
    abit_data["class"] = ""
    abit_data["city"] = ""
    is_phone_defined = False
    is_address_defined = False
    is_email_defined = False
    is_debug = False
    debug_stage = 0
    is_force_exit = False


def start(message):
    global current_stage
    text = "Здравствуйте! Мы рады, что Вы решили выбрать наш университет!\n" \
           "Данный бот, как видно из его названия, собирает данные об абитуриентах, которые изъявляют желание " \
           "поступить сюда.\n\n<здесь будет ещё текст, я уверен, я просто ничего больше ничего не " \
           "придумал толкового>\n\nВаши данные будут переданы нужным людям. Вы согласны предоставить " \
           "Ваши персональные данные для поступления?"
    markup_choice = types.ReplyKeyboardMarkup(resize_keyboard=True)
    yes = types.KeyboardButton("Да")
    no = types.KeyboardButton("Нет")
    markup_choice.add(yes, no)
    bot.send_message(message.chat.id, text, reply_markup=markup_choice)
    current_stage = "Старт"


def agree(message):
    global current_stage, markup_remove, is_phone_defined, is_email_defined, \
        is_address_defined, is_finished, abit_data, is_force_exit
    if current_stage == "Старт":
        if message.text == "Да":
            text = "Тогда погнали! Для начала скажите, как Вас зовут по фамилии, имени и отчеству?"
            bot.send_message(message.chat.id, text, reply_markup=markup_remove)
            current_stage = "Инициалы"
        elif message.text == "Нет":
            text = "Ну, на нет - и суда нет, как говорится. Тогда не будем Вас беспокоить, до свидания!"
            bot.send_message(message.chat.id, text)
            is_force_exit = True
            finish_session(message)
    elif current_stage == "Инициалы":
        _abit_data = message.text
        temp_string = ""
        is_surname = False
        is_name = False
        is_patronymic = False
        for i in _abit_data:
            if i != " ":
                temp_string += i
            else:
                if not is_surname:
                    abit_data["surname"] = temp_string
                    is_surname = True
                elif not is_name:
                    abit_data["name"] = temp_string
                    is_name = True
                elif not is_patronymic:
                    abit_data["patronymic"] = temp_string
                    is_patronymic = True
                temp_string = ""
        if abit_data["patronymic"] == "":
            abit_data["patronymic"] = None

        text = f"Замечательно! Теперь мы знаем, как к тебе обращаться!\n{abit_data['name']}... Какое красивое имя! " \
               "Из какого города ты приехал(а)?"
        bot.send_message(message.chat.id, text, reply_markup=markup_remove)
        current_stage = "Город"
    elif current_stage == "Город":
        abit_data["city"] = message.text

        text = "Ух ты! Нам интересно, из какой школы ты пришёл(ла)?"
        bot.send_message(message.chat.id, text, reply_markup=markup_remove)
        current_stage = "Школа"
    elif current_stage == "Школа":
        abit_data["school"] = message.text

        text = "Вопрос из той же оперы: из какого класса ты пришёл(ла)?"
        bot.send_message(message.chat.id, text)
        current_stage = "Класс"
    elif current_stage == "Класс":
        abit_data["class"] = message.text

        if not is_admin_choice:
            text = f"Хорошо, {abit_data['name']}! Теперь нам нужно знать, как мы можем с тобой связаться " \
                   "помимо телеграм-бота. Я подвожу к тому, что нам нужны твои контактные данные. " \
                   "Но т.к. мы не можем знать, какие данные ты нам готов(а) предоставить, " \
                   "я предоставляю <b>тебе</b> право выбора.\nВ меню кнопок будут представлены доступные варианты, " \
                   "так что выбирай, что тебе будет комфортнее.\n\n" \
                   "(пока у нас нет определённого списка данных, которые мы должны собирать, поэтому пока так, " \
                   "плавающий выбор данных...)"
            markup_choice = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
            phone = types.KeyboardButton("Телефон")
            email = types.KeyboardButton("Email")
            address = types.KeyboardButton("Адрес проживания")
            phone_email = types.KeyboardButton("И телефон, и email")
            address_email = types.KeyboardButton("И адрес, и email")
            phone_address = types.KeyboardButton("И телефон, и адрес")
            all_data = types.KeyboardButton("Всё сразу")
            markup_choice.add(phone, email, address, phone_email, address_email, phone_address, all_data)
            bot.send_message(message.chat.id, text, parse_mode="html", reply_markup=markup_choice)
            current_stage = "Контактные данные: опрос"
        else:
            text = set_text(message.chat.id, message.text)
            bot.send_message(message.chat.id, text)
            current_stage = "Контактные данные: ввод"
    elif current_stage == "Контактные данные: опрос":
        # TODO: разобраться, как мы будем брать данные: одним залпом (одним сообщением, потом вычленять) или
        #  несколькими (несколькими сообщениями, потом поочерёдно присваивать значения)
        text = set_text(message.chat.id, message.text)
        bot.send_message(message.chat.id, text, reply_markup=markup_remove)
        current_stage = "Контактные данные: ввод"
    elif current_stage == "Контактные данные: ввод":
        is_check_end = fill_fields(message.text)
        if is_check_end:
            if abit_data["phone"] == "error" or abit_data["email"] == "error" or abit_data["address"] == "error":
                error_text = "Где-то ты совершил(а) ошибку! Перепиши, пожалуйста, " \
                             "ещё раз своё сообщение с исправленными данными"
                bot.send_message(message.chat.id, error_text, reply_markup=markup_remove)
            else:
                text = "Спасибо за то, что уделили время! Если возникли какие-либо вопросы или предложения по поводу " \
                       "этого бота обращаться к этому боту или человеку (если вдруг бот будет не работать): " \
                       "@FeedbackAboutBots_bot или @QuizBot_Developer"
                bot.send_message(message.chat.id, text)
                current_stage = "None"
                is_finished = True
