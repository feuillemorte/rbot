from datetime import datetime, timedelta
from dateutil import rrule
from configs.config_reader import get_config

config = get_config()


def convert_to_tuple(data):
    return [tuple(data[i:i + 2]) for i in range(0, len(data), 2)]


def get_date_pairs(data):

    result_date_pairs = []

    for pair in data:
        if len(pair) == 1:
            if pair[0].get('from'):
                a = pair[0]['from']
                b = datetime.utcnow()
            else:
                a = datetime.strptime(
                    '{} {}:00:00'.format(datetime.today().strftime('%Y-%m-%d'), config['redmine']['working_time'][0]),
                    '%Y-%m-%d %H:%M:%S'
                )
                b = pair[0]['to']
        else:
            a = pair[0]['from']
            b = pair[1]['to']

        diff_business_days = list(rrule.rrule(rrule.DAILY,
                                              dtstart=a,
                                              until=b,
                                              byweekday=(rrule.MO, rrule.TU, rrule.WE, rrule.TH, rrule.FR, rrule.SA),
                                              byhour=(int(config['redmine']['working_time'][0]),
                                                      int(config['redmine']['working_time'][1])),
                                              byminute=0,
                                              bysecond=0)
                                  )

        if diff_business_days:
            if diff_business_days[0].strftime('%H:%M:%S') != '{}:00:00'.format(config['redmine']['working_time'][0]):
                diff_business_days = [a] + diff_business_days
            if diff_business_days[-1].strftime('%H:%M:%S') != '{}:00:00'.format(config['redmine']['working_time'][1]):
                diff_business_days.append(b)
        elif a.strftime('%d') == b.strftime('%d'):
            diff_business_days = [a, b]

        diff_business_days = convert_to_tuple(diff_business_days)
        result_date_pairs += diff_business_days

    return result_date_pairs


def get_time_by_status(status_id, journals, day=None, update_author=None):
    status_id = str(status_id)
    dates = {status_id: []}

    for journal in journals:

        for detail in journal['details']:
            is_status = detail['name'] == 'status_id'
            if is_status \
                    and detail['new_value'] == status_id \
                    and (update_author is None or update_author == journal['user']['name']):
                time_work_1 = journal['created_on']
                date_dt_1 = datetime.strptime(time_work_1, "%Y-%m-%dT%H:%M:%SZ")
                if day:
                    if day.strftime('%Y-%m-%d') == date_dt_1.strftime('%Y-%m-%d'):
                        dates[status_id].append({'from': date_dt_1})
                else:
                    dates[status_id].append({'from': date_dt_1})

            if is_status and detail['old_value'] == status_id \
                    and (update_author is None or update_author == journal['user']['name']):
                time_work_2 = journal['created_on']
                date_dt_2 = datetime.strptime(time_work_2, "%Y-%m-%dT%H:%M:%SZ")
                if day:
                    if day.strftime('%Y-%m-%d') == date_dt_2.strftime('%Y-%m-%d'):
                        dates[status_id].append({'to': date_dt_2})
                else:
                    dates[status_id].append({'to': date_dt_2})

    dates_tuple = convert_to_tuple(dates[status_id])

    time_list = []
    for pair in get_date_pairs(dates_tuple):
        a, b = pair

        time_list.append(b - a)

    if not time_list:
        return ''
    return sum(time_list, timedelta())
