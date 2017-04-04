from redmine import Redmine
from configs.config_reader import get_config

from rm import Rm

def resolved_task():
    redmine = Rm()
    project = redmine.project

    resolved = [task.subject for task in project.issues if task.status.name == 'Resolved']
    print(resolved)

resolved_task()