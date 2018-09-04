import logging

from crypto_exchange.api.rest.okex import OKExREST

logger = logging.getLogger(__name__)


class OKExSpot(OKExREST):
    def __init__(self, api_key: str = '', secret_key: str = '', ):
        self._api_key = api_key
        self._secret_key = secret_key
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
        ticker_resource = "ticker.do"
        params = {
            'symbol': symbol
        }

        return self.http_get(ticker_resource, params, self.headers)

    def depth(self, symbol: str, size: int = 200):
        """
        获取币币市场深度
        :param symbol:交易对
        :param size:value:1-200
        :return:asks :卖方深度
                bids :买方深度
        """
        depth_resource = "depth.do"
        params = {
            'symbol': symbol,
            'size': size
        }
        return self.http_get(depth_resource, params, self.headers)

    def trades_info(self, symbol: str, since: int = None):
        """
        获取币币历史交易信息(60条)
        :param symbol: 交易对
        :param since: 交易记录ID，返回数据不包括该记录
        :return:
        """
        trades_resource = "trades.do"
        params = {
            'symbol': symbol
        }

        if since:
            params['since'] = since
        return self.http_get(trades_resource, params, self.headers)

    def k_line(self, symbol: str, k_line_type: str, size: int = None, since: int = None):
        """
        获取币币K线数据
        :param symbol: 交易对
        :param k_line_type: 1min/3min/5min/15min/30min/1day/3day/1week/1hour/2hour/4hour/6hour/12hour
        :param size: 获取数据的条数，默认全部获取
        :param since: 时间戳，返回时间戳以后的数据，默认全部获取
        :return:时间戳，开，高，低，收，交易量
        """
        k_line_resource = 'kline.do'
        params = {
            'symbol': symbol,
            'type': k_line_type,
        }

        if size:
            params['size'] = size
        if since:
            params['since'] = since
        return self.http_get(k_line_resource, params, self.headers)

    def user_info(self):
        """
        获取用户信息
        :return: free:账户余额，freezed:账户冻结余额
        """
        user_info_resource = "userinfo.do"
        params = {
            'api_key': self._api_key
        }
        params['sign'] = self.sign(params)
        return self.http_post(user_info_resource, params, self.headers)

    def trade(self, symbol: str, trade_type: str, price: float, amount: float):
        """
        下单交易
        :param symbol: 交易对
        :param trade_type: 买卖类型
        :param price: 下单价格，市价卖单不传price
        :param amount: 交易数量，市价买单不传amount，市价买单需传peice作为买入总金额
        :return: result:交易成功或失败
                order_id:订单ID
        """
        trade_resource = "trade.do"

        params = {
            'api_key': self._api_key,
            'symbol': symbol,
            'type': trade_type
        }

        if price:
            params['price'] = price
        if amount:
            params['amount'] = amount
        params['sign'] = self.sign(params)

        return self.http_post(trade_resource, params, self.headers)

    def batch_trade(self, symbol: str, orders_data: str, trade_type: str = None):
        """
        批量下单交易
        :param symbol:交易对
        :param trade_type: buy/sell/
        :param orders_data: '[{价格,数量，买卖类型},{}]'
        :return: result任一成功返回true，order_id下单失败返回-1，返回信息与上传信息一致
        """

        bath_trade_resource = "batch_trade.do"
        params = {
            'api_key': self._api_key,
            'symbol': symbol,
            'orders_data': orders_data,
        }
        if trade_type:
            params['type'] = trade_type
        params['sign'] = self.sign(params)

        return self.http_post(bath_trade_resource, params, self.headers)

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
        cancel_order_resource = 'cancel_order.do'
        params = {
            'api_key': self._api_key,
            'symbol': symbol,
            'order_id': order_id,
        }
        params['sign'] = self.sign(params)
        return self.http_post(cancel_order_resource, params, self.headers)

    def order_info(self, symbol: str, order_id: int):
        """
        获取用户订单信息
        :param symbol: 交易对
        :param order_id: 订单ID，-1:未完成订单
        :return: status:-1已撤销，0未成交，1部分成交，2完全成交，3撤单处理中
        """
        order_info_resource = "order_info.do"
        params = {
            'api_key': self._api_key,
            'symbol': symbol,
            'order_id': order_id,
        }
        params['sign'] = self.sign(params)
        return self.http_post(order_info_resource, params, self.headers)

    def orders_info(self, symbol: str, order_id: str, info_type: int):
        """
        批量获取订单信息
        :param symbol: 交易对
        :param order_id: 订单ID
        :param info_type: 查询类型
        :return:
        """
        # 校验参数

        orders_info_resource = "orders_info.do"
        params = {
            'api_key': self._api_key,
            'type': info_type,
            'symbol': symbol,
            'order_id': order_id,
        }
        params['sign'] = self.sign(params)
        return self.http_post(orders_info_resource, params, self.headers)

    def order_history(self, symbol: str, status: int, current_page: int, page_length: int):
        """
        获取历史订单信息
        :param symbol: 交易对
        :param status: 查询状态
        :param current_page: 当前页数
        :param page_length: 每页条数
        :return:result:返回与否，total:总条数，currency_page:页数，page_length:每页条数，orders:订单列表
        """
        order_history_resource = "order_history.do"
        params = {
            'api_key': self._api_key,
            'symbol': symbol,
            'status': status,
            'current_page': current_page,
            'page_length': page_length,
        }
        params['sign'] = self.sign(params)

        return self.http_post(order_history_resource, params, self.headers)

    def withdraw(self, symbol: str, charge_fee: float, trade_pwd: str, withdraw_address: str, withdraw_amount: float,
                 target: str = 'OKEX'):
        """
        提币
        :param symbol: 交易对
        :param charge_fee: 网路手续费 BTC[0.002，0.005] LTC[0.001，0.2] ETH[0.01] ETC[0.0001，0.2] BCH范围 [0.0005，0.002]
        :param trade_pwd: 交易密码
        :param withdraw_address: 提币认证地址
        :param withdraw_amount: 提币数量
        :param target: 地址类型
        :return: reault withdraw_id
        """
        withdraw_resource = "withdraw.do"
        params = {
            'api_key': self._api_key,
            'symbol': symbol,
            'chargefee': charge_fee,
            'trde_pwd': trade_pwd,
            'withdraw_address': withdraw_address,
            'withdraw_amount': withdraw_amount,
            'target': target,
        }
        params['sign'] = self.sign(params)
        return self.http_post(withdraw_resource, params, self.headers)

    def cancel_withdraw(self, symbol: str, withdraw_id: str):
        """
        取消提币BTC/LTC/ETH/ETC/BCH
        :param symbol:
        :param withdraw_id:
        :return:
        """
        cancel_withdraw_resource = "cancel_withdraw.do"
        params = {
            'api_key': self._api_key,
            'symbol': symbol,
            'withdraw_id': withdraw_id
        }
        params['sign'] = self.sign(params)
        return self.http_post(cancel_withdraw_resource, params, self.headers)

    def withdraw_info(self, symbol: str, withdraw_id: str):
        """
        查询提币BTC/LTC/ETH/ETC/BCH信息
        :param symbol:
        :param withdraw_id:
        :return:
        """
        withdraw_info_resource = "withdraw_info.do"
        params = {
            'api_key': self._api_key,
            'symbol': symbol,
            'withdraw_id': withdraw_id
        }
        params['sign'] = self.sign(params)
        return self.http_post(withdraw_info_resource, params, self.headers)

    def account_records(self, symbol: str, account_type: int, current_page: int, page_length: int):
        """
        获取用户提现/充值记录
        :param symbol:
        :param account_type:
        :param current_page:
        :param page_length:
        :return:
        """
        account_records = "account_records.do"
        params = {
            'api_key': self._api_key,
            'symbol': symbol,
            'type': account_type,
            'current_page': current_page,
            'page_length': page_length,
        }
        params['sign'] = self.sign(params)

        return self.http_post(account_records, params, headers=self.headers)

    def funds_transfer(self, symbol: str, amount: int, funds_from: int, funds_to: int):
        """
        资金划转
        :param symbol:
        :param amount:
        :param funds_from:
        :param funds_to:
        :return:
        """
        funds_transfer = "funds_transfer.do"
        params = {
            'api_key': self._api_key,
            'symbol': symbol,
            'amount': amount,
            'from': funds_from,
            'to': funds_to,
        }
        params['sign'] = self.sign(params)

        return self.http_post(funds_transfer, params, headers=self.headers)

    def wallet_info(self):
        """
        获取用户钱包账户信息
        :return: free:账户余额，freezed:账户冻结余额
        """
        wallet_info_resource = "wallet_info.do"
        params = {
            'api_key': self._api_key,
        }
        params['sign'] = self.sign(params)
        return self.http_post(wallet_info_resource, params, self.headers)
