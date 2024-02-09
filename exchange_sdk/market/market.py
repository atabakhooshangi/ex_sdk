from ..client.client import Client


class exchangeMarketData(Client):
    def get_orderbook(self, **kwargs):
        params = {}
        if kwargs:
            params.update(kwargs)
        return self._request('GET', f'{self.TRADING}{self.API_V1_STR}/order/order_book/', params=params)

    def get_trade_history(self, **kwargs):
        params = {}
        if kwargs:
            params.update(kwargs)
        return self._request('GET', f'{self.TRADING}{self.API_V1_STR}/trade/', params=params)

    def get_currencies(self):
        return self._request('GET', f'/consul/v1/kv/exchange/coins/?keys=true')

    def get_currency_data(self,coin:str):
        return self._request('GET', f'/consul/v1/kv/exchange/coins/{coin}?raw=true')
