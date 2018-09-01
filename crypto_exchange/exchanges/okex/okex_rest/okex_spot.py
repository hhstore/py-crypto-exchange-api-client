import logging
from crypto_exchange.api.rest.okex import OKExREST

logger = logging.getLogger(__name__)


class OKExSpot(OKExREST):
    def __init__(self, api_key='', secret_key='', ):
        self.__api_key = api_key
        self.__secret_key = secret_key
        self.headers = {
            "Content-type": "application/x-www-form-urlencoded",
        }
        super(OKExSpot, self).__init__(api_key, secret_key)

    def ticker(self, symbol: str):
        """
        获取币币行情数据
        :param symbol: 交易对
        :return:date: 返回数据时服务器时间
                buy: 买一价
                high: 最高价
                last: 最新成交价
                low: 最低价
                sell: 卖一价
                vol: 成交量(最近的24小时)
        """
        TICKER_RESOURCE = "ticker.do"
        params = {
            'symbol': symbol
        }

        return self.http_get(TICKER_RESOURCE, params, self.headers)

    def depth(self, symbol: str, size=200):
        """
        获取币币市场深度
        :param symbol:交易对
               size:value:1-200
        :return:asks :卖方深度
                bids :买方深度
        """
        DEPTH_RESOURCE = "depth.do"
        params = {
            'symbol': symbol
        }

        try:
            if 1 <= size <= 200:
                params['size'] = size
        except Exception as e:
            logger.error(e)
        return self.http_get(DEPTH_RESOURCE, params, self.headers)

    def tradesinfo(self, symbol: str, since=None):
        """
        获取币币历史交易信息(60条)
        :param symbol: 交易对
        :param since: 交易记录ID，返回数据不包括该记录
        :return:
        """
        TRADES_RESOURCE = "trades.do"
        params = {
            'symbol': symbol
        }
        if since:
            params['since'] = since
        return self.http_get(TRADES_RESOURCE, params, self.headers)

    def kine(self, symbol: str, type: str, size=None, since=None):
        """
        获取币币K线数据
        :param symbol: 交易对
        :param type: 1min/3min/5min/15min/30min/1day/3day/1week/1hour/2hour/4hour/6hour/12hour
        :param size: 获取数据的条数，默认全部获取
        :param since: 时间戳，返回时间戳以后的数据，默认全部获取
        :return:时间戳，开，高，低，收，交易量
        """
        KLINE_RESOURCE = 'kline.do'
        params = {
            'symbol': symbol,
            'type': type,
        }
        if size:
            params['size'] = size
        if since:
            params['since'] = since
        return self.http_get(KLINE_RESOURCE, params, self.headers)

    def userinfo(self):
        """
        获取用户信息
        :return: free:账户余额，freezed:账户冻结余额
        """
        USERINFO_RESOURCE = "userinfo.do"
        params = {
            'api_key': self.__api_key
        }
        params['sign'] = self.sign(params)
        return self.http_post(USERINFO_RESOURCE, params, self.headers)

    def wallet_info(self):
        """
        获取用户钱包账户信息
        :return: free:账户余额，freezed:账户冻结余额
        """
        WALLET_INFO_RESOURCE = "wallet_info.do"
        params = {
            'api_key': self.__api_key,
        }
        params['sign'] = self.sign(params)
        return self.http_post(WALLET_INFO_RESOURCE, params, self.headers)

    def trade(self, symbol: str, type: str, price: float, amount: float):
        """
        下单交易
        :param symbol: 交易对
        :param type: 买卖类型
        :param price: 下单价格，市价卖单不传price
        :param amount: 交易数量，市价买单不传amount，市价买单需传peice作为买入总金额
        :return: result:交易成功或失败
                order_id:订单ID
        """
        TRADE_RESOURCE = "trade.do"

        params = {
            'api_key': self.__api_key,
            'symbol': symbol,
            'type': type
        }

        if price:
            params['price'] = price
        if amount:
            params['amount'] = amount
        params['sign'] = self.sign(params)

        return self.http_post(TRADE_RESOURCE, params, self.headers)

    def batch_trade(self, symbol: str, orders_data: str, type=None):
        """
        批量下单交易
        :param symbol:交易对
        :param type: buy/sell/
        :param order_data: '[{价格,数量，买卖类型},{}]'
        :return: result任一成功返回true，order_id下单失败返回-1，返回信息与上传信息一致
        """

        BATH_TRADE_RESOURCE = "batch_trade.do"
        params = {
            'api_key': self.__api_key,
            'symbol': symbol,
            'type': type,
            'orders_data': orders_data,
        }
        params['sign'] = self.sign(params)

        return self.http_post(BATH_TRADE_RESOURCE, params, self.headers)

    def cancel_order(self, symbol: str, order_id: str):
        """
        撤销币币订单
        :param symbol: 交易对
        :param order_id: 订单ID，多个以','分隔，一次最多撤销三个
        :return: result,order_id,success(多笔),error(多笔失败的ID)
        """
        # 校验参数
        if len(order_id.split(',')) > 3:
            raise 1 - 3
        CANCEL_ORDER_RESOURCE = 'cancel_order.do'
        params = {
            'api_key': self.__api_key,
            'symbol': symbol,
            'order_id': order_id,
        }
        params['sign'] = self.sign(params)
        return self.http_post(CANCEL_ORDER_RESOURCE, params, self.headers)

    def order_info(self, symbol, order_id: int):
        """
        获取用户订单信息
        :param symbol: 交易对
        :param order_id: 订单ID，-1:未完成订单
        :return: status:-1已撤销，0未成交，1部分成交，2完全成交，3撤单处理中
        """
        ORDER_INFO_RESOURCE = "order_info.do"
        params = {
            'api_key': self.__api_key,
            'symbol': symbol,
            'order_id': order_id,
        }
        params['sign'] = self.sign(params)
        return self.http_post(ORDER_INFO_RESOURCE, params, self.headers)

    def orders_info(self, symbol, order_id: str, type: int):
        """
        批量获取订单信息
        :param symbol: 交易对
        :param order_id: 订单ID
        :param type: 查询类型
        :return:
        """
        # 校验参数

        ORDERS_INFO_RESOURCE = "orders_info.do"
        params = {
            'api_key': self.__api_key,
            'type': type,
            'symbol': symbol,
            'order_id': order_id,
        }
        params['sign'] = self.sign(params)
        return self.http_post(ORDERS_INFO_RESOURCE, params, self.headers)

    def order_history(self, symbol, status: int, current_page: int, page_length: int):
        """
        获取历史订单信息
        :param symbol: 交易对
        :param status: 查询状态
        :param current_page: 当前页数
        :param page_length: 每页条数
        :return:result:返回与否，total:总条数，currency_page:页数，page_length:每页条数，orders:订单列表
        """
        ORDER_HISTORY_RESOURCE = "order_history.do"
        params = {
            'api_key': self.__api_key,
            'symbol': symbol,
            'status': status,
            'current_page': current_page,
            'page_length': page_length,
        }
        params['sign'] = self.sign(params)

        return self.http_post(ORDER_HISTORY_RESOURCE, params, self.headers)

    def withdraw(self, symbol, chargefee, trade_pwd, withdraw_address, withdraw_amount, target='OKEX'):
        """
        提币
        :param symbol: 交易对
        :param chargefee: 网路手续费 BTC[0.002，0.005] LTC[0.001，0.2] ETH[0.01] ETC[0.0001，0.2] BCH范围 [0.0005，0.002]
        :param trade_pwd: 交易密码
        :param withdraw_address: 提币认证地址
        :param withdraw_amount: 提币数量
        :param target: 地址类型
        :return: reault withdraw_id
        """
        WITHDRAW_RESOURCE = "withdraw.do"
        params = {
            'api_key': self.__api_key,
            'symbol': symbol,
            'chargefee': chargefee,
            'trde_pwd': trade_pwd,
            'withdraw_address': withdraw_address,
            'withdraw_amount': withdraw_amount,
            'target': target,
        }
        params['sign'] = self.sign(params)
        return self.http_post(WITHDRAW_RESOURCE, params, self.headers)
