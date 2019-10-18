from config import Config
from apiClientCaller import ApiClientCaller

class Login:
    email = None
    password = None

    def __init__(self):
        config = Config()
        self.email = config.get_param('Credentials', 'biwenger.mail')
        self.password = config.get_param('Credentials', 'biwenger.pass')

    def get_token(self, cli: ApiClientCaller):
        resp = cli.login(self)
        token = resp["data"]["login"]["token"]
        print("Login successfully done for " + self.email)
        return token
