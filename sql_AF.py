import sqlite3
from datetime import datetime

conn = sqlite3.Connection("abiturients_folder.db", check_same_thread=False)
cur = conn.cursor()
current_datetime = str(datetime.now().day) + "." + str(datetime.now().month) + "." + \
                   str(datetime.now().year) + " " + str(datetime.now().hour) + ":" + \
                   str(datetime.now().minute) + ":" + str(datetime.now().second)


def check_tables():
    """
        This function creates tables if they have not been created
    """
    cur.execute("""CREATE TABLE IF NOT EXISTS students (
        id INTEGER,
        name TEXT,
        surname TEXT,
        patronymic TEXT,
        phone INTEGER,
        email TEXT,
        address TEXT,
        school TEXT,
        class TEXT,
        city TEXT
    )""")
    cur.execute("""CREATE TABLE IF NOT EXISTS sent_messages (
        id INTEGER,
        message_text TEXT,
        write_datetime TEXT
    )""")
    conn.commit()


def get_info_from_abiturient(user_id: int, name: str, surname: str, op_patronymic: str,
                             op_phone: int, op_email: str, op_address: str,
                             school: str, op_class: str, city: str):
    """
        Adds data about student from arguments
    """
    cur.execute("INSERT INTO students (id, name, surname, patronymic, phone, email, address, school, class, city) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (user_id, name, surname, op_patronymic, op_phone, op_email, op_address, school, op_class, city))
    conn.commit()


def get_info_about_message(user_id: int, text: str):
    """
        Adds data about sent message from arguments
    """
    cur.execute("INSERT INTO sent_messages (id, message_text, write_datetime) VALUES (?, ?, ?)",
                (user_id, text, current_datetime))
    conn.commit()


def clear_table(table: str):
    """
        Clear the table specified in the arguments. Returns str, if the operation was successful
    """
    if table in ["students", "sent_messages"]:
        data = ""
        if table == "students":
            cur.execute("DELETE FROM students")
            data = cur.fetchall()
        elif table == "sent_messages":
            cur.execute("DELETE FROM sent_messages")
            data = cur.fetchall()
        conn.commit()
        return data
    else:
        raise SystemError("Задано неправильное название таблицы!")


def test():
    """
        Test function. Do not use in main program
    """
    while True:
        command = input("Введите команду: ")
        if command == "clear":
            table = input("Какую таблицу Вы хотите очистить? ")
            r = clear_table(table)
            print(r)
        elif command == "add_st":
            get_info_from_abiturient(7357, "Аотвщ", "Адащат", "Test", 89023232920, "fgh@eidm.ru", "пер. Гоголевский, 2",
                                     "Пиздец №20", "5a", "Краснодар")
        elif command == "add_se":
            get_info_about_message(7357, "mf_test")
        elif command == "/exit":
            return "Тест функций прошёл успешно!"
        else:
            return "Неверная команда!"


if __name__ == "__main__":
    test_result = test()
    print(test_result)
