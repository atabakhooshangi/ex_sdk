from ..client.client import Client
from decimal import Decimal
from typing import Union
from ..exceptions  import exchangeAuthenticationException


class exchangeTradeOrder(Client):

    def create_order(self, coin: str, pair: str, side: str, type: str, unit_price: Union[Decimal, float],
                     quantity: Union[Decimal, float],
                     **kwargs):
        params = {
            "dest_wallet": coin,
            "origin_wallet": pair,
            "type": side,
            "trade_type": type,
            "unit_price": unit_price,
            "quantity": quantity
        }

        if kwargs:
            params.update(kwargs)
        try:
            resp = self._request('POST', f'{self.TRADING}{self.API_V1_STR}/order/', params=params, auth=True)

        # except exchangeAuthenticationException:
        #     resp = self._request('POST', f'{self.TRADING}{self.API_V1_STR}/order/', params=params, auth=True)
        except Exception as e:
            raise e

        return resp

    def cancel_order(self, order_id: int):
        try:
            resp = self._request('DELETE', f'{self.TRADING}{self.API_V1_STR}/order/cancel_order/{order_id}/', auth=True)
        except exchangeAuthenticationException:
            resp = self._request('DELETE', f'{self.TRADING}{self.API_V1_STR}/order/cancel_order/{order_id}/', auth=True)
        return resp

    def get_my_orders(self, **kwargs):
        """
               :param status__in: status choices : in_progress , success
               :type status__in: string
               :param dest_wallet: coin
               :type dest_wallet: string
               :param origin_wallet:pair
               :type origin_wallet: string
               :param page: page number
               :type page: int
               :param size: page size
               :type size: int
               """
        params = {}
        if kwargs:
            params.update(kwargs)
        print(params)
        try:
            resp = self._request('GET', f'{self.TRADING}{self.API_V1_STR}/order/me/', params=params, auth=True)
            return resp
        except exchangeAuthenticationException:
            resp = self._request('GET', f'{self.TRADING}{self.API_V1_STR}/order/me/', params=params, auth=True)
            return resp
        except Exception as e:
            print(e)

