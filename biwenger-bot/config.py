import configparser
from apiClientCaller import ApiClientCaller

class Config:

    def __init__(self):
        self.config = configparser.RawConfigParser()
        #self.config.read('bot.ini')
        self.config.read('../bot_local.ini')

    def get_param(self, category, key):
        return self.config.get(category, key)

    def wave(self):
        return self.get_param('Wave', 'init.message'

    @staticmethod
    def update_db(cli: ApiClientCaller):
        print("======== ======== CONFIG BUSINESS STARTED ======== ========")
        print("======== Getting all alias information from players in league ========")
        print(cli.update_players_alias())
        print("======== All alias information from players got ========")
        print("======== ======== CONFIG BUSINESS ENDED ======== ========")
