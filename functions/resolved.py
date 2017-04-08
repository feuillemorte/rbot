from configs.config_reader import get_config
from framework.chat_checker import ChatChecker
from rm import Rm

config = get_config()


def resolved_task(bot, update):
    if not ChatChecker().check_chat(update):
        return
    redmine = Rm()
    project = redmine.project

    text = '<b>Следующие задачи решены:</b>\n\n'

    resolved = [task for task in project.issues if task.status.name == config['redmine']['status_resolved']]

    for task in resolved:
        text += '<a href="{}/issues/{}">[{}]</a> - {}\n'.format(
        			config['redmine']['redmine_url'], task.id, task.id, task.subject
        		)

    bot.sendMessage(update.message.chat_id, text, parse_mode='HTML')
