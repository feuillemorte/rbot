def greet_user(bot, update):
	print('AAA')
	print(update)
	bot.sendMessage(
		update.message.chat_id,
		'Доступные команды:\n\n'
		'/resolved решена текст\n'
		'/worktime трудозатраты\n'
		'/who Кто чем занят?\n'
		'/myworkчто я делал за день?\n'
		'/прогнозирование задач\n'
		'/group статистика отдела\n'
		)
