from rm import Rm
from configs.config_reader import get_config

config = get_config()

Rm.update_project()
tasks = [task for task in Rm.project.issues if Rm.project.issues.status.name == config['redmine']['status_resolved']]

# ==

tasks = []
for task in Rm.project.issues:
	if Rm.project.issues.status.name == config['redmine']['status_resolved']:
		tasks.append(task)
