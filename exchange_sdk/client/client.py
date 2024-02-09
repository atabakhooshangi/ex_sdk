import json
import logging
import os
from typing import Dict, Optional, List, Tuple
import requests
import time
from urllib.parse import urlencode, urljoin
from ..exceptions  import exchangeAuthenticationException
from decouple import Config, RepositoryEnv


# DOTENV_FILE = '.env'
# config = Config(RepositoryEnv(DOTENV_FILE))
# path_to_json_config = "config.json"


class Client:
    API_V1_STR: str = "/api/v1"
    IAM_URL: str = os.environ.get("IAM_URL")
    ACCOUNTING_URL: str = os.environ.get("ACCOUNTING_URL")
    TRADING_URL: str = os.environ.get("TRADING_URL")
    ACCOUNTING = 'accounting'
    TRADING = 'trading'
    IAM = 'iam'
    CONSUL = 'consul'
    TOKEN: str = None
    URL: str
    USERNAME: str = None
    PASSWORD: str = None
    PATH_TO_JSON_CONFIG: str = None
    SANDBOX: bool

    def __init__(self, username: str = None, password: str = None, token: str = None,
                 url: str = '', path_to_json_config: str = "",
                 is_sandbox: bool = False):
        self.PATH_TO_JSON_CONFIG = path_to_json_config
        self.SANDBOX = is_sandbox
        if url:
            self.URL = url
        else:
            if is_sandbox:
                self.URL = 'http://0.0.0.0:8000'
            else:
                self.URL = os.environ.get('DOMAIN')
        print(self.IAM_URL)
        if username and password:
            self.USERNAME = username
            self.PASSWORD = password

        if token:
            self.TOKEN = token
        # else:
        #     # try:
        #     #     conf_file = open(self.PATH_TO_JSON_CONFIG)
        #     #     conf_data = json.load(conf_file)
        #     #     token = conf_data['token']
        #     #     if token:
        #     #         self.TOKEN = conf_data['token']
        #     # except KeyError:
        #     #     raise Exception("token does not declared in config")
        #     # except Exception as e:
        #     #     raise e
        #     try:
        #         self.authenticate(username=self.USERNAME, password=self.PASSWORD)
        #         self.TOKEN = token
        #     except Exception as e:
        #
        #         raise e

    def _request(self, method, uri, timeout=15, auth=False, params=None):

        data_json = ''
        if method in ['GET', 'DELETE']:
            if params:
                strl = []
                for key in sorted(params):
                    strl.append("{}={}".format(key, params[key]))
                data_json += '&'.join(strl)
                uri += '?' + data_json
        else:
            if params:
                data_json = json.dumps(params)

        headers = {
            "Content-Type": "application/json"
        }

        if auth:
            if not self.TOKEN:
                self.TOKEN = self.authenticate()['access_token']
            headers["Authorization"] = f"Bearer {self.TOKEN}"
        if self.SANDBOX:
            url_choices = {
                'IAM':os.environ.get("IAM_URL"),
                "ACC": os.environ.get("ACCOUNTING_URL"),
                "TRA": os.environ.get("TRADING_URL")
            }
            print(f"domain : {os.environ.get('DOMAIN')}")
            self.URL = url_choices["IAM" if 'iam' in uri else "TRA" if "trading" in uri else "ACC"]
            uri = uri.split("/")
            uri.pop(0)
            uri = "/".join(uri)

        url = urljoin(self.URL, uri)
        print('absolute url',url)
        try:
            if method in ['GET', 'DELETE']:
                response_data = requests.request(method, url, timeout=timeout, headers=headers, params=params)
            else:
                response_data = requests.request(method, url, headers=headers, data=data_json, timeout=timeout)
        except Exception as e:
            print(f'sdk 1 : {e}')
            raise e

        return self._response_handler(response_data)

    def _response_handler(self, response_data):
        if response_data.status_code == 200:
            print(f'sdk 2')
            try:
                data = response_data.json()
                print(f'sdk 3')
            except ValueError:
                print(f'sdk 4')
                raise Exception(response_data.text)
            try:
                print(f'sdk 5')
                return data['result']
            except KeyError:
                print(f'sdk 6')
                return data
        if response_data.status_code == 204:
            return response_data
        if response_data.status_code == 401:
            # self.authenticate(username=self.USERNAME,password=self.PASSWORD)
            # raise exchangeAuthenticationException(401, "Not authorized")
            return response_data
        raise Exception(response_data.text)
        #     else:
        #         if data and data.get('code'):
        #             if data.get('code') == '200000':
        #                 if data.get('data'):
        #                     return data['data']
        #                 else:
        #                     return data
        #             else:
        #                 raise Exception("{}-{}".format(response_data.status_code, response_data.text))
        # else:
        #     raise Exception("{}-{}".format(response_data.status_code, response_data.text))

    def authenticate(self):

        params = {}
        if self.USERNAME is None and self.PASSWORD is None:

            try:
                conf_file = open(self.PATH_TO_JSON_CONFIG)
                conf_data = json.load(conf_file)
                username = conf_data['username']
                password = conf_data['password']

                if username == "" or password == "":
                    raise KeyError

                params.update({
                    "input": username,
                    "password": password
                })

            except KeyError:
                raise Exception("username or password does not declared or is empty in config file")
        else:
            params.update({
                "input": self.USERNAME,
                "password": self.PASSWORD
            })
        print(self.USERNAME)
        print(self.PASSWORD)

        uri = f'{self.IAM}{self.API_V1_STR}/auth/login/'

        try:
            token = self._request('POST', uri, params=params)
        except Exception as e:
            print(e)
        print(token)
        self.TOKEN = token

        return token

    def refresh_token(self):
        try:
            with open(self.PATH_TO_JSON_CONFIG, 'r+') as f:
                data = json.load(f)
                token = data['token']
                token = self._request('POST', f'{self.IAM}/{self.API_V1_STR}/auth/refresh-token/',
                                      params={"token": token})
                data['token'] = token['access_token']
                f.seek(0)
                json.dump(data, f, indent=4)
                f.truncate()

        except Exception as e:
            raise e
