from login import Login
from config import Config
import requests
import json


class BiwengerApiClient:
    token = None
    headers = None

    def __init__(self, email, password):
        config = Config()
        self.BASEURL = config.get_param('API', 'base.url')
        login = Login(email, password)
        resp = self.do_post('login', login)
        token = resp["data"]["login"]["token"]
        self.token = token
        self.headers = {'Authorization': 'Bearer ' + self.token}

    def do_get(self, endpoint, params=None):
        resp = requests.get(self.BASEURL + endpoint, params=params, headers=self.headers).json()
        #print(resp)
        return resp

    def do_post(self, endpoint, data):
        resp = requests.post(self.BASEURL + endpoint, data=json.dumps(data.__dict__), headers=self.headers).json()
        #print(resp)
        return resp
