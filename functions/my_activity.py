from configs.config_reader import get_config
from framework.chat_checker import ChatChecker
from framework.time_helper import get_time_by_status
from rm import Rm
from datetime import datetime

config = get_config()


def get_activity_for_today(bot, update):
    if not ChatChecker().check_chat(update):
        return

    username = update.message.text.replace('/activity ', '')

    rm = Rm()
    tasks = rm.redmine.issue.filter(updated_on=datetime.today().strftime('=%Y-%m-%d'), include='journals')

    text = '<b>Время на тестирование задач ({}):</b>\n\n'.format(username)

    for task in tasks:
        resolved = get_time_by_status(
            config['redmine']['status_in_qa_id'],
            task.journals.resources,
            datetime.today(),
            update_author=username
        )
        if resolved:
            text += '<a href="{}/issues/{}">[{}]</a> - {} ({})\n'.format(
                config['redmine']['redmine_url'], task.id, task.id, task.subject, resolved
            )

    bot.sendMessage(update.message.chat_id, text, parse_mode='HTML')

