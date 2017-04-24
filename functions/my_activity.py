from configs.config_reader import get_config
from framework.chat_checker import ChatChecker
from framework.time_helper import get_time_by_status
from rm import Rm
from datetime import datetime
from dateutil import rrule

config = get_config()


def get_activity_for_today():

    rm = Rm()
    tasks = rm.redmine.issue.filter(updated_on=datetime.today().strftime('=%Y-%m-%d'), include='journals')

    for task in tasks:
        print(task.subject)
        resolved = get_time_by_status(
            config['redmine']['status_resolved_id'],
            task.journals.resources,
            datetime.today()
        )

        print(resolved)
