import configparser


class Config:

    def __init__(self):
        self.config = configparser.RawConfigParser()
        self.config.read('../bot.ini')
        #self.config.read('../bot_local.ini')

    def get_param(self, category, key):
        return self.config.get(category, key)

    def update_players_alias(self, cli):
        cli.do_get("updatePlayersAlias")
