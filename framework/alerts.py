from telegram.ext import Job
from functions.resolved import get_new_resolved_task
from framework.chat_checker import ChatChecker
from configs.config_reader import get_config

config = get_config()


def callback_timer(bot, update, job_queue):
    if not ChatChecker().check_chat(update):
        return
    bot.sendMessage(chat_id=update.message.chat_id,
                    text='Запущены оповещения')

    new_resolved_tasks = Job(get_new_resolved_task,
                             config['redmine']['job_time'],
                             context=update.message.chat_id
                             )
    job_queue.put(new_resolved_tasks)
