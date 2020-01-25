from apiClientCalls import ApiClientCalls
from login import Login
from config import Config
import requests
import json


class ApiClient:

    def __init__(self):
        self.__BASE_URL = ApiClient.get_base_url()
        self.__headers = self.get_auth_header()

    def do_get(self, endpoint, params=None):
        resp = requests.get(self.BASEURL + endpoint, params=params, headers=self.headers).json()
        #print(resp)
        return resp

    def do_post(self, endpoint, data):
        resp = requests.post(self.BASEURL + endpoint, data=json.dumps(data.__dict__), headers=self.headers).json()
        #print(resp)
        return resp

    @staticmethod
    def __get_base_url():
        config = Config()
        return config.get_param('API', 'base.url')

    def __get_auth_header(self):
        login = Login()
        return {'Authorization': 'Bearer ' + login.get_token(self)}