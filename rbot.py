import logging

from telegram.ext import Updater, CommandHandler

from configs.config_reader import get_config
from functions.greet_user import greet_user
from framework.chat_checker import ChatChecker

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG)


def main():
    config = get_config()
    updater = Updater(config['telegram']['api_token'])

    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start', greet_user))
    dp.add_handler(CommandHandler('pass', ChatChecker().add_chat_to_white_list))

    dp.add_error_handler(show_error)

    updater.start_polling()
    updater.idle()


def show_error(bot, update, error):
    print(error)


main()
