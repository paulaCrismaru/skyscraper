import logging
import os


class Logger(object):

    def __init__(self, name):
        self.logger = logging.getLogger(
            get_file_name(name))
        self.logger.setLevel(logging.DEBUG)

        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)

        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            "%Y-%m-%d %H:%M:%S")
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)

    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def warn(self, message):
        self.logger.warn(message)

    def error(self, message):
        self.logger.error(message)

    def critical(self, message):
        self.logger.critical(message)


def get_file_name(name):
    path_list = name.split(os.sep)
    try:
        index = path_list.index('skyscraper')
        new_path = path_list[index + 1:]
        return os.sep.join(new_path)
    except ValueError:
        return name