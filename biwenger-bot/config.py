import configparser


class Config:

    def __init__(self):
        self.config = configparser.RawConfigParser()
        self.config.read('../bot.ini')

    def get_param(self, category, key):
        return self.config.get(category, key)
