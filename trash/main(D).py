from AF import manager, bot, finish_session

# переменная, которая будет хранить в себе id пользователя, который начал работу с ботом
start_id: int = 0
# переменная, которая будет хранить в себе id пользователей, которые будут начинать работу с ботом
queue_id: list = []
# переменная для обозначения окончания работы пользователя с ботом
is_finished: bool = False


@bot.message_handler(content_types=['text'])
def main(message):
    """
        Here we immediately check if the user is writing to us.
        If yes, then we run the distributing function,
        otherwise we send a message that this user cannot use the bot yet
    """
    # Здесь мы сразу проверяем, тот ли пользователь нам пишет.
    # Если да, то запускаем распределяющую функцию, иначе отправляем сообщение о том,
    # что этот пользователь пока не может пользоваться ботом
    queue_manager(message) if message.from_user.id == start_id or start_id == 0 \
        else bot.send_message(message.from_user.id,
                              "<b>Вы не можете сейчас использовать данную команду.</b>\n"
                              "Более того, <b>Вы не можете сейчас начать работу с данным ботом."
                              "</b>\nВы находитесь в очереди. Мы пришлём Вам сообщение, "
                              "как только другой пользователь закончит работу с ним",
                              parse_mode="html")


def queue_manager(message):
    """
        This feature adds users to the queue to use the bot. Returns True, if user has finished with bot, else False
    """
    # """
    #     Итак, функция queue_manager управляет очередью из пользователей
    #     Принцип работы: мы записываем в определённую переменную message.from_user.id (id пользователя),
    #     который начал программу бота первым и пока один пользователь не закончит, никакой другой пользователь
    #     не может начать работу с ним. Этому пользователю будет выводиться сообщение о том, что сейчас
    #     он не может начать программу бота, т.к. её проходит другой пользователь,
    #     иначе если пользователь выйдет из программы бота, т.е. переменная is_start будет равна False,
    #     его место может занять другой пользователь и так по кругу.
    #
    #     В будущем обновлении планируется сделать реализацию РЕАЛЬНОЙ очереди,
    #     а не её имитации. Её суть проста: каждый пользователь, который не успел начать работу с ботом раньше,
    #     просто переносится в конец очереди, т.е. его id (message.from_user.id) будет помещён
    #     в специальный "массив" (словарь/список). И когда один пользователь закончил работу с ботом, другой пользователь,
    #     стоящий В НАЧАЛЕ очереди (первый элемент в "массиве"), сразу сможет начать с ним работу.
    #
    #     Данная функция нужна, чтобы избегать проблем в логике программы из-за фундаментальной синхронности,
    #     т.к. сообщения будут как радиоволны, накладываться друг на друга и создавать помехи в работе программы бота.
    # """
    global start_id, queue_id, is_finished
    for i in queue_id:
        print(str(queue_id.index(i, 0, int(queue_id.__sizeof__() / 4))) + ", " + str(i) + "; ")
    # если никто ещё не запускал бота, то заполняем переменную id пользователя, который первый начал работу с ботом
    if start_id == 0:
        start_id = message.from_user.id
    # если сообщение пришло от того пользователя, который работает с ботом, то работаем с этим сообщением
    if message.from_user.id == start_id:
        is_finished = manager(message)
    else:
        if start_id != message.from_user.id:
            queue_id.append(message.from_user.id)
    if is_finished and queue_id != []:
        finish_session(message)
        bot.send_message(queue_id[0], "Теперь <b>Вы</b> можете начать работу с ботом!", parse_mode='html')
        start_id = queue_id[0]


if __name__ == "__main__":
    from datetime import datetime

    # используем точное время запуска бота для отладки
    print(str(datetime.now().day) + "." + str(datetime.now().month) + "." +
          str(datetime.now().year) + " " + str(datetime.now().hour) + ":" +
          str(datetime.now().minute) + ":" + str(datetime.now().second))
    bot.polling(non_stop=True, timeout=5, skip_pending=True)
else:
    raise SystemExit("Это главный исполняемый файл, он должен запускаться первым в порядке")
