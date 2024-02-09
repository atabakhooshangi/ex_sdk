from .bot_client import BotClient
from decimal import Decimal
from typing import Union
from ..exceptions import TraderBotAuthenticationException


class exchangeBotOps(BotClient):

    def create_bot(self, **kwargs):
        params = {
        }

        if kwargs:
            params.update(kwargs)
        try:
            resp = self._request('POST', f'trader{self.API_V1_STR}/bots/', params=params)

        except Exception as e:
            raise e

        return resp

    def get_bots(self, **kwargs):
        params = {}
        if kwargs:
            params.update(kwargs)
        try:
            resp = self._request('GET', f'trader{self.API_V1_STR}/bots/', params=params)
        except Exception as e:
            raise e
        return resp

    def update_bot(self, bot_id: int, **kwargs):

        params = {}
        if kwargs:
            params.update(kwargs)
        try:
            resp = self._request('PUT', f'trader{self.API_V1_STR}/bots/{bot_id}/', params=params)
            return resp

        except Exception as e:
            raise e

    def retrieve_bot(self, bot_id):
        try:
            resp = self._request('GET', f'trader{self.API_V1_STR}/bots/{bot_id}/', params={})
            return resp

        except Exception as e:
            raise e
