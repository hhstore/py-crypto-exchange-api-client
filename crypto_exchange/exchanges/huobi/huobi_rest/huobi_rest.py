import logging

from crypto_exchange.api.rest.huobi import HuobiREST

logger = logging.getLogger(__name__)


class HuobiAPI(HuobiREST):
    def __int__(self, api_key: str, secret_key: str):
        self._api_key = api_key
        self._secret_key = secret_key
        super(HuobiAPI, self).__init__(api_key, secret_key)

    def history_k_line(self, symbol: str, period: str, size: int = 150):
        """
        获取K线数据
        :param symbol:
        :param period:
        :param size:
        :return:
        """
        history_k_line_resource = "market/history/kline"
        params = {
            'symbol': symbol,
            'period': period,
            'size': size
        }
        return self.http_get(history_k_line_resource, params)

    def detail_merged(self, symbol: str):
        """
        获取聚合行情
        :param symbol:
        :return:
        """
        detail_merged_resource = "market/detail/merged"
        params = {
            'symbol': symbol
        }
        return self.http_get(detail_merged_resource, params)

    def tickers(self, symbol: str):
        """
        获取行情数据
        :param symbol:
        :return:
        """
        # TODO

    def account(self):
        """
        查询当前用户的所有账户(即account-id)，Pro站和HADAX account-id通用
        :return:
        """
        account_resource = "v1/account/accounts"
        params = {}
        return  self.http_get(account_resource,params)


    def order(self):
        pass
