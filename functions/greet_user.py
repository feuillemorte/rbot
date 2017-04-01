def greet_user(bot, update):
    bot.sendMessage(
        update.message.chat_id,
        """Доступные команды:
        /resolved решена текст
        /worktime трудозатраты
        /who Кто чем занят?
        /mywork что я делал за день?
        /forecast прогнозирование задач
        /group статистика отдела"""
    )
