from datetime import datetime
from dateutil import rrule
from configs.config_reader import get_config
import time


def convert_to_tuple(data):
    return [tuple(data[i:i + 2]) for i in range(0, len(data), 2)]


def get_date_pairs(data):
    config = get_config()

    result_date_pairs = []

    for pair in data:

        if len(pair) == 1:
            a = pair[0]
            b = datetime.now()
        else:
            a, b = pair

        diff_business_days = list(rrule.rrule(rrule.DAILY,
                                              dtstart=a,
                                              until=b,
                                              byweekday=(rrule.MO, rrule.TU, rrule.WE, rrule.TH, rrule.FR),
                                              byhour=(config['redmine']['working_time'][0], config['redmine']['working_time'][1]),
                                              byminute=0,
                                              bysecond=0)
                                  )

        if diff_business_days:
            if diff_business_days[0].strftime('%H:%M:%S') != '{}:00:00'.format(config['redmine']['working_time'][0]):
                diff_business_days = [a] + diff_business_days
            if diff_business_days[-1].strftime('%H:%M:%S') != '{}:00:00'.format(config['redmine']['working_time'][1]):
                diff_business_days.append(b)

        diff_business_days = convert_to_tuple(diff_business_days)
        result_date_pairs += diff_business_days

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
        a, b = pair
        time_list.append((b - a).seconds)
    if not time_list:
        return ''
    return time.strftime('%d день, %H часов, %M минут', time.gmtime(sum(time_list)))
