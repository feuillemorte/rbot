from configs.config_reader import get_config

from rm import Rm

config = get_config()


def resolved_task(bot, update):
    redmine = Rm()

    text = '<b>Следующие задачи решены:</b>\n\n'

    resolved = redmine.redmine.issue.filter(status_id=config['redmine']['status_resolved_id'])

    for task in resolved:
        text += '<a href="{}/issues/{}">[{}]</a> - {}'.format(
                    config['redmine']['redmine_url'], task.id, task.id, task.subject
                )
        developer = ' (Разработчик: )\n'
        for journal in redmine.redmine.issue.get(task.id).journals.resources:
            if journal['details'][0]['new_value'] == '2':
                developer = ' (Разработчик: {})\n'.format(journal['user']['name'])

        text += developer

    bot.sendMessage(update.message.chat_id, text, parse_mode='HTML')
