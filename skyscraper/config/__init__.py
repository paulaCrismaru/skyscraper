import os
import configparser

_DEFAULT_CONFIG_FILES = [
    config_file for config_file in (os.path.join("skyscraper", "config", "skyscraper.conf"),
                                    os.path.join("skyscraper", "skyscraper.conf"))
        if os.path.isfile(os.path.join(os.path.curdir, config_file))
    ]

if os.path.isfile(os.path.join(os.sep, "tmp", "skyscraper.conf")):
    _DEFAULT_CONFIG_FILES.append(
        os.path.join(os.sep, "tmp", "skyscraper.conf"))


class ConfigParser(object):

    def __init__(self, config_file):
        self._config = configparser.ConfigParser()
        self._config.read(config_file)

        for name, section in self._config.items():
            if not hasattr(self, name):
                self._add_section(name)
            self._add_values_to_section(name, section)

    def _add_section(self, name):
        setattr(self, str(name), Section(str(name)))

    def _add_values_to_section(self, name, section):
        getattr(self, name).add_values(section.items())

    @property
    def sections(self):
        param = self.__dict__
        param.pop('_config')
        return param.keys()


class Section(object):

    def __init__(self, name):
        self._name = name

    def add_values(self, values):
        for name, value in values:
            try:
                if float(value) != int(value):
                    setattr(self, name, float(value))
                else:
                    setattr(self, name, int(value))
            except ValueError:
                setattr(self, name, str(value))

    def __repr__(self):
        param = self.__dict__
        param.pop('_name')
        return str(param.items())


if _DEFAULT_CONFIG_FILES:
    CONF = ConfigParser(_DEFAULT_CONFIG_FILES[0])

