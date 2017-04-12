from configs.config_reader import get_config
from framework.chat_checker import ChatChecker
from rm import Rm
from datetime import datetime
from datetime import date, timedelta

config = get_config()


def get_task():
    #if not ChatChecker().check_chat(update):
     #   return
    rm = Rm()

    task = rm.redmine.issue.get(4, include='journals')
    
    for journal in task.journals.resources:
       
        for detail in journal['details']:
            
            if detail['name'] == 'status_id' and detail['new_value'] == '2':
                time_work_1 = journal['created_on']
                date_dt_1 = datetime.strptime(time_work_1, "%Y-%m-%dT%H:%M:%SZ")
                print(date_dt_1)
                print(type(date_dt_1))


            if detail['name'] == 'status_id' and detail['old_value'] == '2' and  detail['new_value'] == '3':
                time_work_2 =  journal['created_on']
                date_dt_2 = datetime.strptime(time_work_2, "%Y-%m-%dT%H:%M:%SZ")


    time_task = date_dt_2 - date_dt_1
    print(time_task)
