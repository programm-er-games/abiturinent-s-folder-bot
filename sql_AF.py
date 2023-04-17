import sqlite3
from datetime import datetime

conn = sqlite3.Connection("abiturient\'s_folder.db", check_same_thread=False)
cur = conn.cursor()
current_datetime = str(datetime.now().day) + "." + str(datetime.now().month) + "." + \
                   str(datetime.now().year) + " " + str(datetime.now().hour) + ":" + \
                   str(datetime.now().minute) + ":" + str(datetime.now().second)


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


def clear_table(table: str):
    if table in ["students", "sent_messages"]:
        data = ""
        if table == "students":
            cur.execute("DROP TABLE students")
            data = cur.fetchall()
        elif table == "sent_messages":
            cur.execute("DROP TABLE sent_messages")
            data = cur.fetchall()
        conn.commit()
        return data
    else:
        raise SystemError("Задано неправильное название таблицы!")


def test():
    while True:
        command = input("Введите команду: ")
        if command == "clear":
            table = input("Какую таблицу Вы хотите очистить? ")
            clear_table(table)
        elif command == "add_st":
            get_info_from_abiturient(7357, "Аотвщ", "Адащат", "Test", 89023232920, "fgh@eidm.ru", "пер. Гоголевский, 2",
                                     "Пиздец №20", "5a", "Краснодар")
        elif command == "add_se":
            get_info_about_message(7357, "mf_test")
        elif command == "/exit":
            return "Тест функций прошёл успешно!"
        else:
            return "Ты долбаёб?"


if __name__ == "__main__":
    test_result = test()
    print(test_result)
