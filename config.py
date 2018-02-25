import logging
import os
from ConfigParser import SafeConfigParser, NoSectionError, NoOptionError
from getpass import getpass
from os.path import expanduser


class Config:
    CONFIG_DIR = expanduser('~') + '/.config/bamboohr'
    CONFIG_FILE = CONFIG_DIR + "/google-calendar-sync.conf"
    BAMBOO_SECTION = 'bamboohr'
    GCAL_SECTION = 'google-calendar'

    config = SafeConfigParser()

    def __init__(self):
        self._read_config()

        if not os.path.exists(self.CONFIG_DIR):
            logging.debug('Creating config directory')
            os.makedirs(self.CONFIG_DIR)

    def _read_config(self):
        self.config.read(self.CONFIG_FILE)
        for section in [self.BAMBOO_SECTION, self.GCAL_SECTION]:
            if section not in self.config.sections():
                self.config.add_section(section)

        try:
            self.bamboo = self.config.items(self.BAMBOO_SECTION)

            # Check all the mandatory things
            c = self.get_config()
            c[self.BAMBOO_SECTION]['company']
            c[self.BAMBOO_SECTION]['employee_id']
            c[self.GCAL_SECTION]['calendar_id']
        except (NoSectionError, NoOptionError, KeyError):
            self._input_config()

    def _input_config(self):
        self.config.set(self.BAMBOO_SECTION, 'company', raw_input('BambooHR Company: '))
        self.config.set(self.BAMBOO_SECTION, 'employee_id', raw_input('Employee ID: '))
        token = raw_input('BambooHR Access Token (leave blank to use username/password): ')
        if token:
            self.config.set(self.BAMBOO_SECTION, 'token', token)
        else:
            logging.debug('No token entered - using username/password')
            self.config.set(self.BAMBOO_SECTION, 'user', raw_input('BambooHR username: '))
            self.config.set(self.BAMBOO_SECTION, 'password', getpass())

        self.config.set(self.GCAL_SECTION, 'calendar_id', raw_input('Google Calendar ID: '))
        self._save()

    def save_token(self, token):
        self.config.set(self.BAMBOO_SECTION, 'token', token)
        # TODO: Clear the username/password?
        self._save()

    def _save(self):
        with open(self.CONFIG_FILE, 'w', 0o600) as configfile:
            self.config.write(configfile)

    def get_config(self):
        return {s: dict(self.config.items(s)) for s in self.config.sections()}


if __name__ == '__main__':
    print Config().get_config()
