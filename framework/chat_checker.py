import yaml

from configs.config_reader import get_config

config = get_config()


class ChatChecker(object):
    def __init__(self):
        self.chat_white_list = self.get_white_list()

    def check_chat(self, update):
        """
        Проверяем есть ли чат в белом списке

        :param update:
        :return:
        """
        if update.message.chat.id in self.chat_white_list:
            return True

    def add_chat_to_white_list(self, bot, update):
        """
        Если пароль правильный, добавляем чат в белый список

        :param bot:
        :param update:
        :return:
        """
        if update.message.text.replace('/pass ', '') == config['telegram']['chat_white_list_password']:
            self.chat_white_list.append(update.message.chat.id)

            data = {'chat_white_list': list(set(self.chat_white_list))}
            with open("configs/white_chat_id_list.yml", 'w') as ymlfile:
                yaml.dump(data, ymlfile, default_flow_style=False)

            bot.sendMessage(
                update.message.chat_id,
                'Теперь вы можете ввести команду /start еще раз для дополнительных функций'
            )

    def get_white_list(self):
        """
        Загрузить белый список из файла

        :return:
        """
        chat_white_list = {}
        try:
            with open("configs/white_chat_id_list.yml", 'r') as ymlfile:
                chat_white_list = yaml.load(ymlfile)
        except FileNotFoundError:
            data = {'chat_white_list': []}
            with open("configs/white_chat_id_list.yml", 'w') as ymlfile:
                yaml.dump(data, ymlfile, default_flow_style=False)

        return chat_white_list.get('chat_white_list', [])
