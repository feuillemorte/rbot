from configs.config_reader import get_config
from framework.chat_checker import ChatChecker
from rm import Rm
from datetime import datetime
from dateutil import rrule
import time
import redmine

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


def convert_to_tuple(data):
    return [tuple(data[i:i + 2]) for i in range(0, len(data), 2)]


def get_date_pairs(data):
    result_date_pairs = []

    for pair in data:
        # print(pair)

        if len(pair) == 1:
            a = pair[0]
            b = datetime.now()
        else:
            a, b = pair

        diff_business_days = list(rrule.rrule(rrule.DAILY,
                                              dtstart=a,
                                              until=b,
                                              byweekday=(rrule.MO, rrule.TU, rrule.WE, rrule.TH, rrule.FR),
                                              byhour=(10, 20), byminute=0)
                                  )

        # print(diff_business_days)
        if a.weekday() != 5 and a.weekday() != 6:
            diff_business_days = [a] + diff_business_days
        if b.weekday() != 5 and b.weekday() != 6:
            diff_business_days.append(b)

        diff_business_days = convert_to_tuple(diff_business_days)
        result_date_pairs += diff_business_days

    # print(result_date_pairs)
    return result_date_pairs


def get_time_by_status(status_id, journals):
    status_id = str(status_id)
    dates = {status_id: []}

    for journal in journals:

        for detail in journal['details']:

            if detail['name'] == 'status_id' and detail['new_value'] == status_id:
                time_work_1 = journal['created_on']
                date_dt_1 = datetime.strptime(time_work_1, "%Y-%m-%dT%H:%M:%SZ")
                dates[status_id].append(date_dt_1)

            if detail['name'] == 'status_id' and detail['old_value'] == status_id:
                time_work_2 = journal['created_on']
                date_dt_2 = datetime.strptime(time_work_2, "%Y-%m-%dT%H:%M:%SZ")
                dates[status_id].append(date_dt_2)

    dates_tuple = convert_to_tuple(dates[status_id])

    time_list = []

    for pair in get_date_pairs(dates_tuple):
        print(pair)
        a, b = pair
        time_list.append((b - a).seconds)

    return time.strftime('%d день, %H часов, %M минут', time.gmtime(sum(time_list)))
