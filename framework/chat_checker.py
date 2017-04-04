from configs.config_reader import get_config

config = get_config()
chat_white_list = config['telegram']['chat_white_list']


class ChatChecker(object):
    def check_chat(self, update):
        """
        Проверяем есть ли чат в белом списке

        :param update:
        :return:
        """
        if update.message.chat.id in chat_white_list:
            return True

    def add_chat_to_white_list(self, bot, update):
        """
        Если пароль правильный, добавляем чат в белый список

        :param bot:
        :param update:
        :return:
        """
        if update.message.text.replace('/pass ', '') == config['telegram']['chat_white_list_password']:
            global chat_white_list
            chat_white_list.append(update.message.chat.id)
            bot.sendMessage(
                update.message.chat_id,
                'Теперь вы можете ввести команду /start еще раз для дополнительных функций'
            )
