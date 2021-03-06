from framework.chat_checker import ChatChecker


def greet_user(bot, update):
    """
    Приветствие пользователя

    :param bot:
    :param update:
    :return:
    """
    if not ChatChecker().check_chat(update):
        bot.sendMessage(
            update.message.chat_id,
            """Доступные команды:
            /pass ввести пароль, ваш чат №{}
            """.format(update.message.chat_id)
        )
        return

    bot.sendMessage(
        update.message.chat_id,
        """Доступные команды:
        /start_alerts запустить оповещения
        /resolved решена текст
        /who Кто чем занят?
        /activity имя пользователя в редмайн
        /task № задачи
        """
    )
