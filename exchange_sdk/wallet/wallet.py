from ..client.client import Client
from decimal import Decimal
from typing import Union
from ..exceptions import exchangeAuthenticationException


class exchangeWallet(Client):

    def get_my_wallets(self):

        try:
            resp = self._request('GET', f'{self.ACCOUNTING}{self.API_V1_STR}/wallet/', params={}, auth=True)

        except exchangeAuthenticationException:
            resp = self._request('GET', f'{self.ACCOUNTING}{self.API_V1_STR}/wallet/', params={}, auth=True)

        return resp
