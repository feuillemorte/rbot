from configs.config_reader import get_config
from framework.chat_checker import ChatChecker
from rm import Rm

config = get_config()


def tasks_for_user(bot, update):
    if not ChatChecker().check_chat(update):
        return
    rm = Rm()
    text = ''
    for user_id in config['redmine']['user_ids']:
        user = rm.redmine.user.get(user_id)
        text += '<b>{} {}</b>\n\n'.format(user.firstname, user.lastname)
        for task in user.issues:
            text += '<a href="{}/issues/{}">[{}]</a> - {} ({})\n'.format(
                config['redmine']['redmine_url'], task.id, task.id, task.subject, task.status.name
            )

    bot.sendMessage(update.message.chat_id, text, parse_mode='HTML')
