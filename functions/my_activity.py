from configs.config_reader import get_config
from framework.chat_checker import ChatChecker
from framework.time_helper import get_time_by_status
from rm import Rm
from datetime import datetime

config = get_config()


def get_activity_for_today(bot, update):
    """
    Функция для определения активности пользователя за день (тестирование)

    :param bot:
    :param update:
    :return:
    """
    if not ChatChecker().check_chat(update):
        return

    username = update.message.text.replace('/activity', '')
    username = username.strip()

    if not username:
        bot.sendMessage(update.message.chat_id, 'Введите имя пользователя')
        return

    rm = Rm()
    # фильтруем задачи по значению updated_on
    tasks = rm.redmine.issue.filter(updated_on=datetime.today().strftime('=%Y-%m-%d'), include='journals')

    text = '<b>Время на тестирование задач ({}):</b>\n\n'.format(username)

    # Перебираем задачи, возвращаем время по статусу config['redmine']['status_in_qa_id'] за сегодня
    for task in tasks:
        time_in_qa = get_time_by_status(
            config['redmine']['status_in_qa_id'],
            task.journals.resources,
            day=datetime.today(),
            update_author=username
        )
        if time_in_qa:
            text += '<a href="{}/issues/{}">[{}]</a> - {} ({})\n'.format(
                config['redmine']['redmine_url'], task.id, task.id, task.subject, time_in_qa
            )

    bot.sendMessage(update.message.chat_id, text, parse_mode='HTML')

