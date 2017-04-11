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
        /resolved решена текст
        /worktime трудозатраты
        /who Кто чем занят?
        /mywork что я делал за день?
        /forecast прогнозирование задач
        /group статистика отдела
        /task № задачи
        """
    )
