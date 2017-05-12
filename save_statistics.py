from configs.config_reader import get_config
from datetime import datetime
from framework.base_user import db_session, Statistics
from framework.time_helper import get_time_by_status
from rm import Rm

config = get_config()

rm = Rm()
# фильтруем задачи по значению updated_on
tasks = rm.redmine.issue.filter(updated_on=datetime.today().strftime('=%Y-%m-%d'), include='journals')

list_users = config['redmine']['usernames']

for user in list_users:

    # Перебираем задачи, возвращаем время по статусу config['redmine']['status_in_qa_id'] за сегодня
    for task in tasks:
        time_in_qa = get_time_by_status(
            config['redmine']['status_in_qa_id'],
            task.journals.resources,
            day=datetime.today(),
            update_author=user
        )
            
        if time_in_qa:
            st = Statistics(
                user_name=user,
                issue_id=task.id,
                issue_subject=task.subject,
                time_issue=time_in_qa,
                day=datetime.today()
            )

            db_session.add(st)
            db_session.commit()

