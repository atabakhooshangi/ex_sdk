import os
import json
from typing import Dict, Optional, List, Tuple
import requests
import time
from urllib.parse import urlencode, urljoin
from ..exceptions import TraderBotAuthenticationException


class BotClient:
    API_KEY: str
    BASE_URL: str
    API_V1_STR: str = "/api/v1"
    TEST: bool = False

    def __init__(self, api_key: str, test: bool = False):
        self.BASE_URL = os.environ.get('DOMAIN')
        self.API_KEY = api_key
        print(f"bot domain : {os.environ.get('DOMAIN')}")
        # if base_url:
        #     self.BASE_URL = base_url
        if test:
            self.TEST = test
            self.BASE_URL = os.environ.get('TRADER_BOT_URL')

        print(f"base url : {self.BASE_URL}")

    def _request(self, method, uri, timeout=15, params=None):

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
            "Content-Type": "application/json",
            "exchange-API": self.API_KEY
        }
        if self.TEST:
            uri = uri.split("/")
            uri.pop(0)
            uri = "/".join(uri)

        url = urljoin(self.BASE_URL, uri)
        print(url)
        try:
            if method in ['GET', 'DELETE']:
                response_data = requests.request(method, url, timeout=timeout, headers=headers, params=params)
            else:
                response_data = requests.request(method, url, headers=headers, data=data_json, timeout=timeout)
                print(response_data.status_code)
        except Exception as e:
            raise e

        return self._response_handler(response_data)

    def _response_handler(self, response_data):
        if response_data.status_code == 200:
            try:
                data = response_data.json()
            except ValueError:
                raise Exception(response_data.text)
            return data['result']
        if response_data.status_code == 204:
            return response_data
        if response_data.status_code == 401:
            raise TraderBotAuthenticationException(401, "Not authorized")
