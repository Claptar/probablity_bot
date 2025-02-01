import logging.config
import yaml


def setup_logging():
    with open("app/utils/logging_config.yml", "r") as file:
        config = yaml.safe_load(file.read())
        logging.config.dictConfig(config)
