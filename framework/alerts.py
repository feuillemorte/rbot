from telegram.ext import Job
from functions.resolved import get_new_resolved_task
from framework.chat_checker import ChatChecker


def callback_timer(bot, update, job_queue):
    if not ChatChecker().check_chat(update):
        return
    bot.sendMessage(chat_id=update.message.chat_id,
                    text='Setting a timer for 1 minute!')

    new_resolved_tasks = Job(get_new_resolved_task,
                             60.0,
                             context=update.message.chat_id
                             )
    job_queue.put(new_resolved_tasks)
