from redmine import Redmine
from configs.config_reader import get_config


class Rm(object):
    def __init__(self):
        config = get_config()

        self.redmine = Redmine(
            config['redmine']['redmine_url'],
            username=config['redmine']['username'],
            password=config['redmine']['password']
        )
        self.project = None
        self.update_project()
      

    def update_project(self):
        config = get_config()
        self.project = self.redmine.project.get(config['redmine']['project_name'])
        
        