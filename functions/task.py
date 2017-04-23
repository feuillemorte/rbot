import redmine

from configs.config_reader import get_config
from framework.chat_checker import ChatChecker
from rm import Rm
from framework.time_helper import get_time_by_status

config = get_config()


def get_task(bot, update):
    if not ChatChecker().check_chat(update):
        return

    rm = Rm()

    task_id = update.message.text.replace('/task ', '')
    task_id = task_id.replace('/task{} '.format(config['telegram']['bot_name']), '')

    try:
        task_id = int(task_id)
    except ValueError:
        bot.sendMessage(update.message.chat_id, 'Введите номер задачи')
        return

    try:
        task = rm.redmine.issue.get(task_id, include='journals')
    except redmine.exceptions.ResourceNotFoundError:
        bot.sendMessage(update.message.chat_id, 'Задача не найдена')
        return

    in_progress = get_time_by_status(config['redmine']['status_in_progress_id'], task.journals.resources)
    resolved = get_time_by_status(config['redmine']['status_resolved_id'], task.journals.resources)

    text = '<b>Затраченное время на задачу:</b>\n\n<b>В работе:</b> {}\n<b>В статусе решена:</b> {}'.format(
        in_progress, resolved
    )

    bot.sendMessage(update.message.chat_id, text, parse_mode='HTML')
