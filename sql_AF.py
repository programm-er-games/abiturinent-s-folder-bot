import sqlite3
from datetime import datetime

conn = sqlite3.Connection("abiturient\'s_folder.db", check_same_thread=False)
cur = conn.cursor()
current_datetime = str(datetime.now().day) + "." + str(datetime.now().month) + "." + str(datetime.now().year) + " " + str(datetime.now().hour) + ":" + str(datetime.now().minute) + ":" + str(datetime.now().second)


def get_info_from_abiturient(user_id: int, name: str, surname: str, op_patronymic: str,
                             op_phone: int, op_email: str, op_address: str,
                             school: str, op_class: str, city: str):
    cur.execute("INSERT INTO students (id, name, surname, patronymic, phone, email, address, school, class, city) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (user_id, name, surname, op_patronymic, op_phone, op_email, op_address, school, op_class, city))
    conn.commit()


def get_info_about_message(user_id: int, text: str):
    cur.execute("INSERT INTO sent_messages (id, message_text, write_datetime) VALUES (?, ?, ?)",
                (user_id, text, current_datetime))
    conn.commit()
