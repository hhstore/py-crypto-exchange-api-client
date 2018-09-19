import logging
import time

from crypto_exchange.utils.rest.bitmex import BitMexREST

logger = logging.getLogger(__name__)


class BitMexFuture(BitMexREST):
    def __init__(self, api_key: str = '', secret_key: str = '', url: str = None
                 ):
        self._api_key = api_key
        self._secret_key = secret_key
        self._url = url if url else "https://www.bitmex.com/api/v1"
        self.headers = {
            "Content-type": "application/x-www-form-urlencoded",
        }
        super(BitMexFuture, self).__init__(api_key, secret_key, url=url)

    async def get_order(self, symbol: str, filters: str = None, columns: str = None, count: float = 100,
                        start: float = None,
                        reverse: bool = False, start_time: time = None, end_time: time = None, ):
        """
        获取订单信息
        :param symbol:
        :param filters:
        :param columns:
        :param count:
        :param start:
        :param reverse:
        :param start_time:
        :param end_time:
        :return:
        """
        get_order_resource = 'order'
        params = {
            'symbol': symbol,
            'reverse': reverse,
            'count': count
        }

        if filters:
            params['filter'] = filters
        if columns:
            params['columns'] = columns
        if start:
            params['start'] = start
        if start_time:
            params['startTime'] = start_time
        if end_time:
            params['endTime'] = end_time

        # 有延迟，时间戳+2
        expires = int(time.time() + 2)
        expires = str(expires)
        print(expires)
        headers = {
            'Content-Type': 'application/json',
            'api-expires': expires,
            'api-key': self.api_key,
            'api-signature': await self.sign(params, 'GET', self._url, get_order_resource, expires),
        }
        return await self.http_get(get_order_resource, params, headers)

    async def post_order(self, symbol: str, order_side: str, simple_order_qty: float = None, order_qty: float = None,
                         price: float = None,
                         display_qty: float = None, stop_px: float = None, client_order_id: str = None,
                         client_order_link_id: str = None,
                         peg_offset_value: float = None,
                         peg_price_type: str = None, order_type: str = None, time_in_force: str = None,
                         execution_instructions: str = None,
                         contingency_type: str = None,
                         text: str = None):
        """
        下单
        :param symbol: 交易对
        :param order_side: Buy, Sell
        :param simple_order_qty: 以基础币种（即比特币）为单位的订单数量
        :param order_qty: 数量 以币种为单位的订单数量（即合同)
        :param price: 价格 'Limit'，'StopLimit'和'LimitIfTouched'订单的可选限价
        :param display_qty:
        :param stop_px: “Stop”，“StopLimit”，“MarketIfTouched”和“LimitIfTouched”订单的可选触发价格
                        使用低于当前价格的止损卖单和买入触及订单的价格
                        使用execInst'MarkPrice'或'LastPrice'来定义用于触发的当前价格。

        :param client_order_id: 可选的客户订单ID
        :param client_order_link_id:
        :param peg_offset_value:
        :param peg_price_type: 有效选项：LastPeg，MidPricePeg，MarketPeg，PrimaryPeg，TrailingStopPeg
        :param order_type: 订单类型 limit
                                market
                                MarketWithLeftOverAsLimit
                                Stop
                                StopLimit
                                MarketIfTouched
                                LimitIfTouched

                                price指定时默认为“Limit” 。stopPx指定时默认为“Stop” 。何时指定price和stopPx时默认为“StopLimit”

        :param time_in_force: 有效时间 Day，
                                    GoodTillCancel，一直有效直到取消'Limit'，'StopLimit'，'LimitIfTouched'和'MarketWithLeftOverAsLimit'订单，默认为'GoodTillCancel'
                                    ImmediateOrCancel，立刻成交或取消
                                    FillOrKill 完全成交或取消

        :param execution_instructions: 执行指令 ParticipateDoNotInitiate，
                                AllOrNone，要求displayQty为0
                                MarkPrice，
                                IndexPrice，
                                LastPrice，
                                Close，
                                ReduceOnly，
                                Fixed

                                'MarkPrice'，'IndexPrice'或'LastPrice'指令对'Stop'，'StopLimit'，'MarketIfTouched'和'LimitIfTouched'指令有效

        :param contingency_type: 应急类型 OneCancelsTheOther，
                                        OneTriggersTheOther，
                                        OneUpdatesTheOtherAbsolute，
                                        OneUpdatesTheOtherProportional。
        :param text:订单注释
        :return:
        """
        create_order_resource = 'order'
        params = {
            'symbol': symbol,
            'sider': order_side,
            'orderQty': order_qty,
            'ordType': order_type,
        }
        if price is not None:
            params['price'] = price
        if simple_order_qty:
            params['simleOrderQty'] = simple_order_qty
        if display_qty:
            params['displayQty'] = display_qty
        if stop_px:
            params['stopPx'] = stop_px
        if client_order_id:
            params['clOrdID'] = client_order_id
        if client_order_link_id:
            params['clOrdLinkID'] = client_order_link_id
        if peg_offset_value:
            params['pegOffsetValue'] = peg_offset_value
        if peg_price_type:
            params['pegPriceType'] = peg_price_type
        if time_in_force:
            params['timeInForce'] = time_in_force
        if execution_instructions:
            params['execInst'] = execution_instructions
        if contingency_type:
            params['contingencyType'] = contingency_type
        if text:
            params['text'] = text
        # 有延迟，时间戳+2
        expires = int(time.time() + 2)
        expires = str(expires)
        print(expires)
        headers = {
            'Content-Type': 'application/json',
            'api-expires': expires,
            'api-key': self.api_key,
            'api-signature': await self.sign(params, 'POST', self._url, create_order_resource, expires),
        }
        return await self.http_post(create_order_resource, params, headers)

    async def delete_order(self, order_id: str, client_order_id: str, text: str = None):
        """
        撤销订单
        :param order_id:
        :param client_order_id:
        :param text:
        :return:
        """
        pass
