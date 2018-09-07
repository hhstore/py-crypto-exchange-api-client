import logging

from crypto_exchange.utils.rest.huobi import HuobiREST

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

    def tickers(self, symbol: str = None):
        """
        获取行情数据
        :param symbol:
        :return:
        """
        # TODO
        tickers_resource = "market/tickers"
        params = {}
        if symbol:
            params['symbol'] = symbol
        return self.http_get(tickers_resource, params)

    def depth(self, symbol: str, depth_type: str):
        """
        获取 Market Depth 数据
        :param symbol:
        :param depth_type:
        :return:
        """
        depth_resource = "market/depth"
        params = {
            'symbol': symbol,
            'type': depth_type,
        }
        return self.http_get(depth_resource, params)

    def trade_detail(self, symbol: str):
        """
        获取 Trade Detail 数据
        :param symbol:
        :return:
        """
        trade_resource = "market/trade"
        params = {
            'symbol': symbol
        }
        return self.http_get(trade_resource, params)

    def history_trade(self, symbol: str, size: int):
        """
        批量获取最近的交易记录
        :param symbol:
        :param size:
        :return:
        """
        history_trade_resource = "market/history/trade"
        params = {
            'symbol': symbol,
            'size': size
        }
        return self.http_get(history_trade_resource, params)

    def trade_24_detail(self, symbol: str):
        """
        获取 Market Detail 24小时成交量数据
        :param symbol:
        :return:
        """
        trade_24_detail_resource = "market/detail"
        params = {
            'symbol': symbol
        }
        return self.http_get(trade_24_detail_resource, params)

    def symbols(self, site: str = None):
        """
        默认 查询Pro站支持的所有交易对及精度
        查询HADAX站支持的所有交易对及精度

        :return:
        """
        common_symbols_resource = "v1/common/symbols"
        if site == 'hadax':
            common_symbols_resource = "v1/hadax/common/symbols"
        params = {}
        return self.http_get(common_symbols_resource, params, sign=False)

    def currency(self, site: str = None):
        """
        默认 查询Pro站支持的所有币种
        查询HADAX站支持的所有币种
        :param site:
        :return:
        """
        common_currencys_resource = "v1/common/currencys"
        if site == 'hadax':
            common_currencys_resource = "v1/hadax/common/currencys"
        params = {}
        return self.http_get(common_currencys_resource, params, sign=False)

    def timestamp(self):
        """
        查询系统当前时间
        :return:
        """
        common_timestamp = "v1/common/timestamp"
        params = {}
        return self.http_get(common_timestamp, params, sign=False)

    def account(self):
        """
        查询当前用户的所有账户(即account-id)，Pro站和HADAX account-id通用
        :return:
        """
        account_resource = "v1/account/accounts"
        params = {}
        return self.http_get(account_resource, params)

    def account_balance(self, account_id: str, site: str = None):
        """
        默认 查询Pro站指定账户的余额
        查询HADAX站指定账户的余额
        :param account_id:
        :param site
        :return:
        """
        account_balance_resource = "v1/account/accounts/{}/balance".format(account_id)
        if site == 'hadax':
            account_balance_resource = "v1/hadax/account/accounts/{}/balance".format(account_id)
        params = {}
        return self.http_get(account_balance_resource, params)

    def orders_place(self, account_id: str, amount: str, source: str, symbol: str, order_type: str,
                     price: int = 0,
                     site: str = None):
        """
        默认 Pro站下单
        HADAX站下单
        :param account_id:
        :param symbol:
        :param order_type:
        :param amount:
        :param price:
        :param source:
        :param site:
        :return:
        """
        orders_place_resource = "v1/order/orders/place"
        if site == 'hadax':
            orders_place_resource = "v1/hadax/order/orders/place"

        params = {"account-id": account_id,
                  "amount": amount,
                  "symbol": symbol,
                  "type": order_type,
                  "source": source}
        if price:
            params["price"] = price
        return self.http_post(orders_place_resource, params, )

    def open_orders(self, account_id: str, symbol: str, side: str = None, size: int = 10):
        """
        获取所有当前帐号下未成交订单
        :param account_id:
        :param symbol:
        :param side:
        :param size:
        :return:
        """
        open_orders_resource = "v1/order/openOrders"
        params = {
            'account-id': account_id,
            'symbol': symbol,
            'size': size
        }
        if side:
            params['side'] = side
        return self.http_get(open_orders_resource, params)

    def cancel_order(self, order_id: str):
        """
        申请撤销一个订单请求
        :param order_id:
        :return:
        """
        cancel_order_resource = "v1/order/orders/{}/submitcancel".format(order_id)
        return self.http_post(cancel_order_resource)

    def batch_cancel_orders(self, orders_id: list):
        """
        批量撤销订单
        :param orders_id:
        :return:
        """
        params = {
            'order-ids': orders_id
        }
        batch_cancel_orders_resource = "v1/order/orders/batchcancel"
        return self.http_post(batch_cancel_orders_resource, params)

    def batch_cancel_open_orders(self, account_id: str, symbol: str = None, side: str = None, size: int = 10):
        """
        批量取消符合条件的订单
        :param account_id:
        :param symbol:
        :param side:
        :param size:
        :return:
        """
        # TODO
