from configs.config_reader import get_config
from framework.chat_checker import ChatChecker
from rm import Rm

config = get_config()


def get_task():
    #if not ChatChecker().check_chat(update):
     #   return
    rm = Rm()

    task = rm.redmine.issue.get(16)
    for journal in task.journals.resources:
        print(journal)
