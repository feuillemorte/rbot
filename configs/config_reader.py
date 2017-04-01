import yaml


def get_config():
    with open("configs/config.yml", 'r') as ymlfile:
        config = yaml.load(ymlfile)
    return config
