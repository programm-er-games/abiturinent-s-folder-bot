# 13.04.2023 5:00 - я написал почти с нуля логику сценария, кроме SQL-части,
#  основной программы (без менеджера очередей) с 0:00

"""
    Как добавить какой-либо этап в код, не поломав при этом ничего? Всё очень просто!
    Т.к. поэтапная система завязана на переменной current_stage, то мы просто следуем за этими шагами:
        1. Придумайте название этапа такое, чтобы оно отображало суть Вашего вопроса. Нам нужна читабельность кода,
        поэтому нужно использовать 1 слово. Если не получилось, то можно использовать 2-3 слова, не больше
        (обычно используется в случаях, когда сам этап предполагает ответвления -
        разные действия под одинаковым предлогом);
        2. Придумайте текст, который Вы собираетесь выводить на этом этапе;
        3. Продумайте логику, которая будет исполняться ПОСЛЕ того, как пользователь отправит "ответ" на Ваш "вопрос";
        Теперь, когда мы знаем, что именно мы хотим добавить в этап, мы идём дальше, а именно к самому коду:
            Если мы собираемся создавать этап в конце всей программы, то:
                4. Пишем в конце блока с условием последнего этапа то,
                что мы хотим написать пользователю (текст из шага 2);
                5. Пишем в конце функции условие elif current_stage == "[название из шага 1]": (или конструкцию else,
                если по логике этапа необходимо исключающее условие, но никак не if, потому что он сломает всю
                целостность структуры и будет "лететь вперёд паровоза", т.е. собьётся порядок);
                6. В блоке условия из шага 5 мы пишем логику из шага 3 и переход на нулевой
                этап (current_stage = "None").
            Если мы собираемся создавать этап между двумя существующими ("один" и "два"), то:
                (здесь алгоритм чуть сложнее объяснить, но суть алгоритма та же)
                4. В конце кода этапа "один" мы прописываем то, что мы хотим написать пользователю (текст из шага 2);
                5. Между этапом "один" и "два" прописываем условие elif current_stage == "[название из шага 1]":
                (никак не if, потому что он сломает всю целостность структуры и
                будет "лететь вперёд паровоза", т.е. собьётся порядок);
                6. В блоке условия из шага 5 мы пишем логику из шага 3.
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
is_phone_defined = False
is_address_defined = False
is_email_defined = False
is_debug = False
is_finished = False
variables_list = {
    "p_d": types.KeyboardButton("is_phone_defined"),  # , callback_data="p_d"
    "e_d": types.KeyboardButton("is_email_defined"),  # , callback_data="e_d"
    "a_d": types.KeyboardButton("is_address_defined"),  # , callback_data="a_d"
    "message_list": ...,
    "markup_choice": types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    # "chat_id": 0
}
debug_stage = 0


# TODO: сделать распределяющую функцию; не забыть, что на этапе "Старт" есть выбор "Да" или "Нет",
#  что необходимо учесть при выборе вариантов развития событий


def manager(message):
    get_info_about_message(message.chat.id, message.text)
    if message.text == "/about":
        about(message)
    elif message.text == "/admin" or debug_stage > 0:
        admin(message)
    elif current_stage == "None":
        start(message)
    elif current_stage in ["Старт", "Инициалы", "Город", "Школа, класс",
                           "Контактные данные: опрос", "Контактные данные: ввод"]:
        agree(message)

    elif current_stage not in ["None", "Старт", "Инициалы", "Город", "Школа, класс",
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
    global debug_stage, is_debug, is_phone_defined, is_email_defined, is_address_defined
    if not is_debug:
        if debug_stage == 0:
            bot.send_message(message.chat.id, "Ты разработчик? Докажи!")
            text = "<b>Первый вопрос:</b> как называется этот проект?"
            bot.send_message(message.chat.id, text, parse_mode='html')

            debug_stage += 1
        elif debug_stage == 1:
            text = ""
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
            text = ""
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
            text = ""
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
                global is_phone_defined, is_email_defined, is_address_defined
                variables_list["markup_choice"].add(variables_list["p_d"], variables_list["e_d"], variables_list["a_d"])
                variables_list["message_list"] = \
                    bot.send_message(message.chat.id, "Эти переменные можно изменить:\n\n"
                                                      f"     is_phone_defined: {is_phone_defined}\n"
                                                      f"     is_email_defined: {is_email_defined}\n"
                                                      f"     is_address_defined: {is_address_defined}\n"
                                                      "\nВ меню кнопок выбирай переменную, значение которой хочешь "
                                                      "поменять на противоположное",
                                     reply_markup=variables_list["markup_choice"])
                # variables_list["chat_id"] = message.chat.id

    else:
        if message.text.startwith("/del"):
            if message.text.endswith("st"):
                clear_table("students")
            elif message.text.endswith("se"):
                clear_table("sent_messages")
        else:
            if message.text == "is_phone_defined":
                is_phone_defined = True if not is_phone_defined else False
            elif message.text == "is_email_defined":
                is_email_defined = True if not is_email_defined else False
            elif message.text == "is_address_defined":
                is_address_defined = True if not is_address_defined else False
            bot.send_message(message.chat.id, "Эти переменные можно изменить:\n\n"
                                              f"     is_phone_defined: {is_phone_defined}\n"
                                              f"     is_email_defined: {is_email_defined}\n"
                                              f"     is_address_defined: {is_address_defined}\n"
                                              "\nВ меню кнопок выбирай переменную, значение которой "
                                              "хочешь поменять на противоположное",
                             reply_markup=variables_list["markup_choice"])
# @bot.callback_query_handler(func=lambda c: c.data == "p_d")
# def change_phone_define(callback_query: types.CallbackQuery):
#     global is_phone_defined
#     bot.answer_callback_query(callback_query.id)
#     # далее мы делаем действия, связанные с этой кнопкой по сценарию
#     if is_debug:
#         if not is_phone_defined:
#             is_phone_defined = True
#         else:
#             is_phone_defined = False
#         bot.edit_message_text(chat_id=variables_list["chat_id"], message_id=variables_list["message_list"].id,
#                               text=variables_list["text_list"], reply_markup=variables_list["markup_choice"])
#
#
# @bot.callback_query_handler(func=lambda c: c.data == "e_d")
# def change_email_define(callback_query: types.CallbackQuery):
#     global is_email_defined
#     bot.answer_callback_query(callback_query.id)
#     # далее мы делаем действия, связанные с этой кнопкой по сценарию
#     if is_debug:
#         if not is_email_defined:
#             is_email_defined = True
#         else:
#             is_email_defined = False
#         bot.edit_message_text(chat_id=variables_list["chat_id"], message_id=variables_list["message_list"].id,
#                               text=variables_list["text_list"], reply_markup=variables_list["markup_choice"])
#
#
# @bot.callback_query_handler(func=lambda c: c.data == "a_d")
# def change_address_define(callback_query: types.CallbackQuery):
#     global is_address_defined
#     bot.answer_callback_query(callback_query.id)
#     # далее мы делаем действия, связанные с этой кнопкой по сценарию
#     if is_debug:
#         if not is_address_defined:
#             is_address_defined = True
#         else:
#             is_address_defined = False
#         bot.edit_message_text(chat_id=variables_list["chat_id"], message_id=variables_list["message_list"].id,
#                               text=variables_list["text_list"], reply_markup=variables_list["markup_choice"])


def non_admin(message):
    global debug_stage, is_debug
    debug_stage = 0
    is_debug = False
    manager(message)


def finish_session(message):
    global current_stage, is_phone_defined, \
        is_email_defined, is_address_defined, \
        is_debug, debug_stage, abit_data
    get_info_from_abiturient(message.chat.id, abit_data["name"], abit_data["surname"],
                             abit_data["patronymic"], abit_data["phone"], abit_data["email"],
                             abit_data["address"], abit_data["school"], abit_data["class"],
                             abit_data["city"])
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
        is_address_defined, is_finished, abit_data
    if current_stage == "Старт":
        text = "Тогда погнали! Для начала скажите, как Вас зовут по фамилии, имени и отчеству?"
        bot.send_message(message.chat.id, text, reply_markup=markup_remove)
        current_stage = "Инициалы"
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
    elif current_stage == "Контактные данные: опрос":
        # TODO: разобраться, как мы будем брать данные: одним залпом (одним сообщением, потом вычленять) или
        #  несколькими (несколькими сообщениями, потом поочерёдно присваивать значения)
        text = ""
        if message.text == "Телефон":
            text = "Тогда напиши, пожалуйста, свой рабочий номер телефона, чтобы мы всегда могли тебе позвонить " \
                   "и спросить, как у тебя дела :)"
            is_phone_defined = True
        elif message.text == "Email":
            text = "Тогда напиши, пожалуйста, свой рабочий email, чтобы мы всегда могли написать тебе " \
                   "и спросить, как дела с долгами :)"
            is_email_defined = True
        elif message.text == "Адрес проживания":
            text = "Тогда напиши, пожалуйста, свой адрес, где ты прямо сейчас прописан(а), чтобы мы могли найти тебя " \
                   "и к тебе в случае чего придёт военком :)"
            is_address_defined = True
        elif message.text == "И телефон, и email":
            text = "Тогда напиши, пожалуйста, телефон и email через запятую, чтобы бот смог различить данные"
            is_phone_defined, is_email_defined = True
        elif message.text == "И адрес, и email":
            text = "Тогда напиши, пожалуйста, адрес проживания и email через запятую, чтобы бот смог различить данные"
            is_address_defined, is_email_defined = True
        elif message.text == "И телефон, и адрес":
            text = "Тогда напиши, пожалуйста, телефон и адрес проживания через запятую, чтобы бот смог различить данные"
            is_phone_defined, is_address_defined = True
        elif message.text == "Всё сразу":
            text = "Ого! Ты решил(а) всё сразу нам сказать? Какой(ая) ты молодец!\nВ таком случае напиши, " \
                   "пожалуйста, телефон, email и адрес проживания через запятую, чтобы бот смог различить данные"
            is_phone_defined, is_email_defined, is_address_defined = True
        bot.send_message(message.chat.id, text)
        current_stage = "Контактные данные: ввод"
    elif current_stage == "Контактные данные: ввод":
        _abit_data: str = message.text
        temp_string = ""
        for i in _abit_data:
            if (is_phone_defined and is_email_defined) or \
                    (is_address_defined and is_email_defined) or \
                    (is_phone_defined and is_address_defined) or \
                    (is_phone_defined and is_address_defined and is_email_defined):
                if i != ",":
                    temp_string += i
            else:
                if _abit_data.index(i) == _abit_data.__len__():
                    if is_phone_defined:
                        abit_data["phone"] = check_phone_format(temp_string)
                    elif is_email_defined:
                        abit_data["email"] = check_email_format(temp_string)
                    elif is_address_defined:
                        abit_data["address"] = check_address_format(temp_string)
                else:
                    temp_string += i
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
