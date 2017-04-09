from datetime import datetime, timedelta
from configs.config_reader import get_config
from framework.chat_checker import ChatChecker
from rm import Rm

config = get_config()

redmine = Rm()


def send_resolved_task(bot, update):
    """
    Отправляет в чат сообщение о рещенных задачах

    :param bot:
    :param update:
    :return:
    """
    if not ChatChecker().check_chat(update):
        return

    text = '<b>Следующие задачи решены:</b>\n\n'

    text += get_resolved_tasks_text()

    bot.sendMessage(update.message.chat_id, text, parse_mode='HTML')


def get_resolved_tasks_text(updated=None):
    """
    Возвращает текст отфитрованных решенных задач

    :param updated: Время обновления задач в формате %Y-%m-%dT%H:%M:%SZ
    :return: string
    """
    resolved_tasks = redmine.redmine.issue.filter(
        status_id=config['redmine']['status_resolved_id'], updated_on=updated
    )

    text = ''
    for task in resolved_tasks:
        text += '<a href="{}/issues/{}">[{}]</a> - {}'.format(
                    config['redmine']['redmine_url'], task.id, task.id, task.subject
                )
        developer = ' (Разработчик: )\n'
        for journal in redmine.redmine.issue.get(task.id).journals.resources:
            if journal['details'][0]['new_value'] == str(config['redmine']['status_in_progress_id']):
                developer = ' (Разработчик: {})\n'.format(journal['user']['name'])

        text += developer

    return text


def get_new_resolved_task(bot, job):
    """
    Оповещение о новой задаче в пуле

    :param bot:
    :param job:
    :return:
    """
    last_time = datetime.now() - timedelta(hours=3, seconds=config['redmine']['updated_time'])
    last_time = datetime.strftime(last_time, '%Y-%m-%dT%H:%M:%SZ')

    text = '<b>Новая задача в пуле:</b>\n\n'

    text_resolved_tasks = get_resolved_tasks_text('>={}'.format(last_time))

    if text_resolved_tasks:
        text += text_resolved_tasks
        bot.sendMessage(job.context, text, parse_mode='HTML')
