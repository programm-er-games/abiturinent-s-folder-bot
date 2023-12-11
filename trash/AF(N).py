# 13.04.2023 5:00 - я написал почти с нуля логику основной программы (без менеджера очередей) с 0:00

import telebot
from telebot import types
from config import abit_sfedu_bot
from check_formats_AF import check_phone_format, check_email_format, check_address_format

bot = telebot.TeleBot(abit_sfedu_bot)
markup_remove = types.ReplyKeyboardRemove()
current_stage = "None"
abit_name: str
abit_surname: str
abit_patronymic: str = ""
abit_phone: int
abit_address: str
abit_email: str
abit_school: str
abit_class: str
abit_city: str
is_phone_defined = False
is_address_defined = False
is_email_defined = False
is_debug: False

# TODO: сделать распределяющую функцию; не забыть, что на этапе "Старт" есть выбор "Да" или "Нет",
#  что необходимо учесть при выборе вариантов развития событий


"""
    Как добавить какой-либо этап в код, не поломав при этом ничего? Всё очень просто!
    Т.к. поэтапная система завязана на переменной current_stage, то мы просто следуем за этими шагами:
        1. Придумайте название этапа такое, чтобы оно отображало суть Вашего вопроса. Нам нужна читабельность кода, 
        поэтому нужно использовать 1 слово. Если так не получилось, то можно использовать 2-3 слова, не больше
        (обычно используется в случаях, когда сам этап предполагает ответвления - 
        разные действия под одинаковым предлогом);
        2. Придумайте текст, который Вы собираетесь выводить на этом этапе ;
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


@bot.message_handler(content_types=['text'])
def manager(message):
    if current_stage == "None":
        start(message)
    elif current_stage in ["Старт", "Инициалы", "Город", "Контактные данные: опрос", "Контактные: ввод"]:
        agree(message)
    else:
        bot.send_message(message.chat.id, "<b>Извините, возникли неполадки в программе. "
                                          "Выполняю принудительное завершение работы...</b>", parse_mode='html')
        bot.stop_bot()
        raise SystemError("Сбой в программе! Неправильное название этапа!")


@bot.message_handler(commands=['about'])
def about(message):
    global markup_remove
    text = "Данный бот создан замечательным, но скромным человеком Поповым Алексеем Эдуардовичем " \
           "на собственном энтузиазме. По вопросам или предложениям по поводу этого бота " \
           "обращаться к этому боту или человеку (если вдруг бот будет не работать): " \
           "@FeedbackAboutBots_bot или @QuizBot_Developer"
    bot.send_message(message.chat.id, text, reply_markup=markup_remove)


def start(message):
    global current_stage
    text = "Здравствуйте! Мы рады, что Вы решили выбрать наш университет!\n" \
           "Данный бот, как видно из его названия, собирает данные об абитуриентах, которые изъявляют желание " \
           "поступить сюда.\n\n<здесь будет ещё текст, я уверен, я просто ничего больше ничего не " \
           "придумал толкового>\n\nВаши данные будут переданы нужным людям. Вы согласны предоставить " \
           "Ваши персональные данные для поступления?"
    markup_choice = types.ReplyKeyboardMarkup()
    yes = types.KeyboardButton("Да")
    no = types.KeyboardButton("Нет")
    markup_choice.add(yes, no)
    bot.send_message(message.chat.id, text, reply_markup=markup_choice)
    current_stage = "Старт"


def agree(message):
    global current_stage, markup_remove, abit_surname, abit_patronymic, \
        abit_name, abit_city, abit_school, abit_class,  is_phone_defined, \
        is_email_defined, is_address_defined, abit_phone, abit_email, abit_address
    if current_stage == "Старт":
        text = "Тогда погнали! Для начала скажите, как Вас зовут по фамилии, имени и отчеству?"
        bot.send_message(message.chat.id, text, reply_markup=markup_remove)
        current_stage = "Инициалы"
    elif current_stage == "Инициалы":
        _abit_name = message.text
        temp_string = ""
        is_surname = False
        is_name = False
        is_patronymic = False
        for i in _abit_name:
            if i != " ":
                temp_string += i
            else:
                if not is_surname:
                    abit_surname = temp_string
                    is_surname = True
                elif not is_name:
                    abit_name = temp_string
                    is_name = True
                elif not is_patronymic:
                    abit_patronymic = temp_string
                    is_patronymic = True
                temp_string = ""
        if abit_patronymic == "":
            abit_patronymic = None

        text = f"Замечательно! Теперь мы знаем, как к тебе обращаться!\n{abit_name}... Какое красивое имя! Из какого" \
               f"города ты приехал(а)?"
        bot.send_message(message.chat.id, text, reply_markup=markup_remove)
    elif current_stage == "Город":
        abit_city = message.text

        text = "Ух ты! Нам интересно, из какой школы ты пришёл(ла) и, " \
               "если не сложно, какого класса(через запятую после школы, пожалуйста)?"
        bot.send_message(message.chat.id, text, reply_markup=markup_remove)
        current_stage = "Школа, класс"
    elif current_stage == "Школа, класс":
        _abit_school = message.text
        temp_string = ""
        is_school = False
        is_class = False
        for i in _abit_school:
            if i != "," or (i != " " and not is_school and is_class):
                temp_string += i
            else:
                if not is_school:
                    abit_school = temp_string
                    is_school = True
                elif not is_class:
                    abit_class = temp_string
                    is_class = True
                temp_string = ""

        text = f"Хорошо, {abit_name}! Теперь нам нужно знать, как мы можем с тобой связаться помимо телеграм-бота. " \
               "Я подвожу к тому, что нам нужны твои контактные данные. Но т.к. мы не можем знать, какие " \
               "данные ты нам готов(а) предоставить, я предоставляю <b>тебе</b> право выбора.\n" \
               "В меню кнопок будут представлены доступные варианты, так что выбирай, что тебе будет комфортнее.\n\n" \
               "<пока у нас нет определённого списка данных, которые мы должны собирать, поэтому пока так, " \
               "плавающий выбор данных...>"
        # TODO: здесь надо решить какой вид клавиатуры нам нужно настроить: reply или inline клавиатура
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
            text = "Тогда напиши, пожалуйста, свой адрес, где ты прямо сейчас прописана, чтобы мы могли найти тебя " \
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
        _abit_data = message.text
        temp_string = ""
        for i in _abit_data:
            if i != "," and is_address_defined:
                temp_string += i
            else:
                if is_phone_defined:
                    abit_phone = check_phone_format(temp_string)
                elif is_email_defined:
                    abit_email = check_email_format(temp_string)
                elif is_address_defined:
                    abit_address = check_address_format(temp_string)
        if abit_phone == "error" or abit_email == "error" or abit_address == "error":
            error_text = "Где-то ты совершил(а) ошибку! Перепиши, пожалуйста, " \
                         "ещё раз своё сообщение с исправленными данными"
            bot.send_message(message.chat.id, error_text, reply_markup=markup_remove)
        else:
            text = "Спасибо за то, что уделили время! Если возникли какие-либо вопросы или предложения по поводу " \
                   "этого бота обращаться к этому боту или человеку (если вдруг бот будет не работать): " \
                   "@FeedbackAboutBots_bot или @QuizBot_Developer"
            bot.send_message(message.chat.id, text)
            current_stage = "None"
