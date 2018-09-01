import logging

from crypto_exchange.api.rest.okex import OKExREST

logger = logging.getLogger(__name__)


class OKExFuture(OKExREST):
    def __init__(self, api_key='', secret_key='', ):
        self._api_key = api_key
        self._secret_key = secret_key
        self.headers = {
            "Content-type": "application/x-www-form-urlencoded",
        }
        super(OKExFuture, self).__init__(api_key, secret_key)

    def future_ticker(self, symbol: str, contract_type: str):
        """
        获取合约行情数据
        :param symbol:交易对
        :param contract_type:合约类型: this_week:当周 next_week:下周 quarter:季度
        :return:buy:买一价
                contract_id:合约ID
                high:最高价
                last:最新成交价
                low:最低价
                sell:卖一价
                unit_amount:合约面值
                vol:成交量(最近的24小时)
        """
        future_ticker_resource = 'future_ticker.do'
        params = {
            'symbol': symbol,
            'contract_type': contract_type
        }
        return self.http_get(future_ticker_resource, params, self.headers)

    def future_depth(self, symbol: str, contract_type: str, size: int, merge=0):
        """
        获取合约深度信息
        :param symbol: 交易对
        :param contract_type: 合约类型: this_week:当周 next_week:下周 quarter:季度
        :param size:value：1-200
        :param merge:value：1(合并深度)，默认0
        :return:asks :卖方深度
                bids :买方深度
        """
        future_depth_resource = "future_depth.do"
        params = {
            'symbol': symbol,
            'contract_type': contract_type,
            'size': size,
            'merge': merge
        }

        return self.http_get(future_depth_resource, params, self.headers)

    def future_trades(self, symbol: str, contract_type: str):
        """
        获取合约交易记录信息
        :param symbol:
        :param contract_type:
        :return:
        """
        future_trades_resource = 'future_trades.do'
        params = {
            'symbol': symbol,
            'contract_type': contract_type
        }
        return self.http_get(future_trades_resource, params, self.headers)

    def future_index(self, symbol: str):
        """
        获取合约指数信息
        :param symbol:
        :return:
        """
        future_index_resource = 'future_index.do'
        params = {
            'symbol': symbol
        }
        return self.http_get(future_index_resource, params, self.headers)

    def future_estimated_price(self, symbol: str):
        """
        获取交割预估价
        :param symbol:
        :return:
        """
        future_estimated_price_resource = "future_estimated_price.do"
        params = {
            'symbol': symbol
        }
        return self.http_get(future_estimated_price_resource, params, self.headers)

    def future_k_line(self, symbol: str, type: str, contract_type: str, size: int = 0, since: int = 0):
        """
        获取合约K线信息
        :param symbol:
        :param type:
        :param contract_type:
        :param size:
        :param since:
        :return:
        """
        future_k_line_resource = "future_kline.do"
        params = {
            'symbol': symbol,
            'type': type,
            'contract_type': contract_type,
            'size': size,
            'since': since
        }
        return self.http_get(future_k_line_resource, params, self.headers)

    def future_hold_amount(self, symbol: str, contract_type: str):
        """
        获取当前可用合约总持仓量
        :param symbol:
        :param contract_type:
        :return:
        """
        future_hold_amount_resource = 'future_hold_amount.do'
        params = {
            'symbol': symbol,
            'contract_type': contract_type
        }
        return self.http_get(future_hold_amount_resource, params, self.headers)

    def future_price_limit(self,symbol: str, contract_type: str):
        """
        获取合约最高限价和最低限价
        :param symbol:
        :param contract_type:
        :return:
        """
        future_price_limit_resource = 'future_price_limit.do'
        params = {
            'symbol': symbol,
            'contract_type': contract_type
        }
        return self.http_get(future_price_limit_resource, params, self.headers)


    def future_user_info(self):
        """
        获取合约账户信息(全仓) 访问频率 10次/2秒
        :return:
        """
        future_user_info = "future_userinfo.do"
        params = {
            'api_key': self._api_key
        }

        params['sign'] = self.sign(params)
        return self.http_post(future_user_info, params, self.headers)

    def future_position(self, symbol: str, contract_type: str):
        """
        获取合约全仓持仓信息 访问频率 10次/2秒
        :param symbol: 交易对
        :param contract_type: 合约类型: this_week:当周 next_week:下周 quarter:季度
        :return:
        """
        future_position = "future_position.do"
        params = {
            'api_key': self._api_key,
            'symbol': symbol,
            'contract_type': contract_type
        }
        params['sign'] = self.sign(params)
        return self.http_post(future_position, params, self.headers)

    def future_trade(self, symbol: str, contract_type: str, price: str, amount: str, trade_type: str, match_price: str,
                     lever_rate: str):
        """
        合约下单 访问频率 5次/1秒(按币种单独计算)
        :param symbol:交易对
        :param contract_type:合约类型
        :param price:价格
        :param amount:委托数量
        :param trade_type:1:开多 2:开空 3:平多 4:平空
        :param match_price:是否为对手价 0:不是 1:是 ,当取值为1时,price无效
        :param lever_rate:杠杆倍数
        :return:
        """
        if match_price == "1":
            price = None
        future_trade = "future_trade.do"
        params = {
            'api_key': self._api_key,
            'symbol': symbol,
            'contract_type': contract_type,
            'amount': amount,
            'type': trade_type,
            'match_price': match_price,
            'lever_rate': lever_rate
        }
        if price:
            params['price'] = price

        params['sign'] = self.sign(params)
        return self.http_post(future_trade, params, self.headers)

    def future_batch_trade(self, symbol: str, contract_type: str, orders_data: str, lever_rate: str):
        """
        合约批量下单 访问频率 3次/1秒 最多一次下1-5个订单（按币种单独计算）
        :param symbol: 交易对
        :param contract_type:合约类型: this_week:当周 next_week:下周 quarter:季度
        :param orders_data:JSON类型的字符串 例：[{price:5,amount:2,type:1,match_price:1},{price:2,amount:3,type:1,match_price:1}] 最大下单量为5，
        :param lever_rate:杠杆倍数
        :return:
        """

        FUTURE_BATCH_TRADE = "future_batch_trade.do"
        params = {
            'api_key': self._api_key,
            'symbol': symbol,
            'contract_type': contract_type,
            'orders_data': orders_data,
            'lever_rate': lever_rate
        }
        params['sign'] = self.sign(params)
        return self.http_post(FUTURE_BATCH_TRADE, params, self.headers)

    def future_cancel(self, symbol: str, contract_type: str, order_id: str):
        """
        取消合约订单 访问频率 2次/1秒，最多一次撤1-5个订单（按币种单独计算）
        :param symbol: 交易对
        :param contract_type: 合约类型: this_week:当周 next_week:下周 quarter:季度
        :param order_id: 订单ID(多个订单ID中间以","分隔,一次最多允许撤消5个订单)
        :return:
        """
        FUTURE_CANCEL = "future_cancel.do"
        params = {
            'api_key': self._api_key,
            'symbol': symbol,
            'contract_type': contract_type,
            'order_id': order_id
        }
        params['sign'] = self.sign(params)
        return self.http_post(FUTURE_CANCEL, params, self.headers)

    def future_trades_history(self, symbol: str, date: str, since: int):
        """
        获取合约交易历史(非个人)访问频率 2次/2秒
        :param symbol: 交易对
        :param date: 合约交割时间，格式yyyy-MM-dd
        :param since:交易Id起始位置
        :return: [{amount：交易数量
                date：交易时间(毫秒)
                price：交易价格
                tid：交易ID
                type：交易类型（buy/sell）},]
        """
        FUTURE_TRADES_HISTORY = "future_trades_history.do"
        params = {
            'api_key': self._api_key,
            'symbol': symbol,
            'date': date,
            'since': since
        }
        params['sign'] = self.sign(params)
        return self.http_post(FUTURE_TRADES_HISTORY, params, self.headers)

    def future_order_info(self, symbol: str, contract_type: str, order_id: str, status: str, current_page: str,
                          page_length: str):
        """
        获取合约订单信息
        :param symbol: 交易对
        :param contract_type:合约类型: this_week:当周 next_week:下周 quarter:季度
        :param order_id:订单ID -1:查询指定状态的订单，否则查询相应订单号的订单
        :param status:查询状态 1:未完成的订单 2:已经完成的订单
        :param current_page:当前页数
        :param page_length:每页获取条数，最多不超过50
        :return:
        """
        FUTURE_ORDERINFO = "future_order_info.do"
        params = {
            'api_key': self._api_key,
            'symbol': symbol,
            'contract_type': contract_type,
            'order_id': order_id,
            'status': status,
            'current_page': current_page,
            'page_length': page_length
        }
        params['sign'] = self.sign(params)
        return self.http_post(FUTURE_ORDERINFO, params, self.headers)

    def future_orders_info(self, symbol: str, contract_type: str, orders_id: str):
        """
        批量获取合约订单信息
        :param symbol: 交易对
        :param contract_type:合约类型: this_week:当周 next_week:下周 quarter:季度
        :param order_id:订单ID(多个订单ID中间以","分隔,一次最多允许查询50个订单)
        :return:
        """
        FUTURE_ORDERS_INFO = "future_orders_info.do"
        params = {
            'api_key': self._api_key,
            'symbol': symbol,
            'contract_type': contract_type,
            'order_id': orders_id
        }
        params['sign'] = self.sign(params)
        return self.http_post(FUTURE_ORDERS_INFO, params, self.headers)

    def future_user_info_4fix(self):
        """
        获取逐仓合约账户信息
        :return:
        """
        FUTURE_INFO_4FIX = "future_userinfo_4fix.do"
        params = {
            'api_key': self._api_key
        }
        params['sign'] = self.sign(params)
        return self.http_post(FUTURE_INFO_4FIX, params, self.headers)

    def future_position_4fix(self, symbol: str, contract_type: str, type=None):
        """
        逐仓用户持仓查询 访问频率 10次/2秒
        :param symbol:交易对
        :param contract_type:合约类型: this_week:当周 next_week:下周 quarter:季度
        :param type:默认返回10倍杠杆持仓 type=1 返回全部持仓数据
        :return:
        """
        FUTURE_POSITION_4FIX = "future_position_4fix.do"
        params = {
            'api_key': self._api_key,
            'symbol': symbol,
            'contract_type': contract_type,
        }
        if type:
            params['type'] = type
        params['sign'] = self.sign(params)
        return self.http_post(FUTURE_POSITION_4FIX, params, self.headers)

    def future_explosive(self, symbol: str, contract_type: str, status: str, current_page=None, page_number=None,
                         page_length=None):
        """
        获取合约爆仓单
        :param symbol: 交易对
        :param contract_type:合约类型: this_week:当周 next_week:下周 quarter:季度
        :param status:状态 0：最近7天未成交 1:最近7天已成交
        :param current_page:当前页数索引值
        :param page_number:当前页数(使用page_number时current_page失效，current_page无需传)
        :param page_length:每页获取条数，最多不超过50
        :return:
        """
        FUTURE_EXPLOSIVE = "future_explosive.do"
        if page_number:
            current_page = None
        params = {
            'api_key': self._api_key,
            'symbol': symbol,
            'contract_type': contract_type,
            'status': status,
        }

        if current_page:
            params['current_page'] = current_page
        if page_number:
            params['page_number'] = page_number
        if page_length:
            params['page_length'] = page_length
        params['sign'] = self.sign(params)
        return self.http_post(FUTURE_EXPLOSIVE, params, self.headers)
