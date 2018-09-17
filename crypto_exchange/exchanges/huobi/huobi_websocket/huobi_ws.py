import gzip
import json
import logging
import time
import datetime
import uuid
from pprint import pprint
from queue import Queue

from websocket import create_connection

logger = logging.getLogger(__name__)

API_KEY = ''
SECRET_KEY = ''

# websocket status
IDLE = 'idle'
GOING_TO_CONNECT = 'going-to-connect'
CONNECTING = 'connecting'
READY = 'ready'
GOING_TO_DICCONNECT = 'going-to-disconnect'


class HuoBiClient(object):

    def __init__(self, api_key=None, secret_key=None):
        self.url = "wss://api.huobipro.com/ws"
        self.ws = None
        self.data = None
        self.queue = Queue()

        self.api_key = api_key or API_KEY
        self.secret_key = secret_key or SECRET_KEY

        self.ws_support = True
        self.last_pong = int(datetime.datetime.utcnow().timestamp()*1000)
        self.closed = False
        self.ws_state = GOING_TO_CONNECT

        self.ws_connect()

    @property
    def is_running(self):
        return not self.closed

    # close
    def close(self):
        if self.ws and not self.ws.closed:
            self.ws.close()
        self.closed = True

    # set ws status
    def set_ws_state(self, new, reason=''):
        print(f'set ws state from {self.ws_state} to {new}', reason)
        self.ws_state = new

    # # keep connection
    # async def keep_connection(self):
    #     while self.is_running:
    #         if not self.ws_support:
    #             break
    #         if self.ws_state == GOING_TO_CONNECT:
    #             self.ws_connect()
    #         elif self.ws_state == READY:
    #             print('ws status ok!')
    #         elif self.ws_state == GOING_TO_DICCONNECT:
    #             self.ws.close()
    #         time.sleep(5)

    # websocket connect
    def ws_connect(self):
        self.set_ws_state(CONNECTING)
        try:
            print(self.url)
            self.ws = create_connection(self.url)
        except Exception as e:
            logger.error(e)
            self.set_ws_state(GOING_TO_CONNECT, 'ws connect failed')
            print('connect ws error,retry...')
            time.sleep(5)
        finally:
            self.set_ws_state(READY)

    def send_sub(self, data):
        """
        订阅数据
        :param data:
        :return:
        """
        self.data = data
        self.ws.send(data)
        pprint('订阅数据')

    def recv(self):
        """
        接收数据
        :return:
        """
        while self.is_running:
            compress_data = self.ws.recv()
            result = gzip.decompress(compress_data).decode('utf-8')

            if result[:7] == '{"ping"':
               self.pong(result)
            else:
                result = json.loads(result)
                print(f'data result:{result}')
                # todo 消息处理

    def un_sub(self, un_sub_data):
        # un_sub_data = re.sub(r'sub', 'unsub', self.data)
        pprint(un_sub_data)
        self.ws.send(un_sub_data)
        pprint('取消订阅')

    # pong
    def pong(self, ping_result):
        """
        :param ping_result: 火币ping的结果
        :return:
        """
        ping = ping_result[8:21]
        pong = '{"pong":' + ping + '}'
        self.last_pong = int(ping)
        self.ws.send(pong)
        print('发送pong')

    # 订阅k线图
    def sub_kline(self, symbol: str, period: str):
        """

        :param symbol: 交易对：ethbtc, ltcbtc, etcbtc, bchbtc
        :param period: 周期：1min, 5min, 15min, 30min, 60min, 1day, 1mon, 1week, 1year
        :return:
            data:
                tick:
                      "tick": {
                          "id": K线id,
                          "amount": 成交量,
                          "count": 成交笔数,
                          "open": 开盘价,
                          "close": 收盘价,当K线为最晚的一根时，是最新成交价
                          "low": 最低价,
                          "high": 最高价,
                          "vol": 成交额, 即 sum(每一笔成交价 * 该笔的成交量)
                      }
        """
        # 订阅 KLine 数据
        channel = """{"sub": "market.%s.kline.%s","id": "id10"}""" % (symbol, period)
        print(f'event :{channel}')
        self.send_sub(channel)
        self.recv()

    def req_kline(self, symbol: str, period: str, start: int=None, end: int=None):
        """
        :param symbol: 交易对：ethbtc, ltcbtc, etcbtc, bchbtc
        :param period: 周期：1min, 5min, 15min, 30min, 60min, 1day, 1mon, 1week, 1year
        :param start: 起始时间
        :param end: 结束时间
        :return:
        """
        # 请求kline数据
        if start and end:
            channel = """{"req": "market.%s.kline.%s","id": "id10", "from": %s, "to": %s}""" % (symbol, period, start, end)
        else:
            channel = """{"req": "market.%s.kline.%s","id": "id10"}""" % (symbol, period)
        print(f'channel :{channel}')
        self.send_sub(channel)
        self.recv()

    # 订阅市场深度(合并深度)
    def sub_market_depth(self, symbol: str, type: str):
        """
        :param symbol: 交易对：btcusdt, ethusdt, ltcusdt, etcusdt, bchusdt, ethbtc, ltcbtc, etcbtc, bchbtc
        :param type: 深度类型：step0, step1, step2, step3, step4, step5（合并深度0-5）；step0时，不合并深度
                    用户选择“合并深度”时，一定报价精度内的市场挂单将予以合并显示（具体合并规则见GET /v1/common/symbols）。合并深度仅改变显示方式，不改变实际成交价。
        :return:
                data:
                    "tick": {
                        "bids": [
                        [买1价,买1量]
                        [买2价,买2量]
                        //more data here
                        ]
                        "asks": [
                        [卖1价,卖1量]
                        [卖2价,卖2量]
                        //more data here
                        ]
                    }
        """
        channel = """{"sub": "market.%s.depth.%s","id": "id1"}""" % (symbol, type)
        print(f'channel :{channel}')
        self.send_sub(channel)
        self.recv()

    # 请求市场深度(合并深度)
    def req_market_depth(self, symbol: str, type: str):
        """
        :param symbol: 交易对：btcusdt, ethusdt, ltcusdt, etcusdt, bchusdt, ethbtc, ltcbtc, etcbtc, bchbtc
        :param type: 深度类型：step0, step1, step2, step3, step4, step5（合并深度0-5）；step0时，不合并深度
                    用户选择“合并深度”时，一定报价精度内的市场挂单将予以合并显示（具体合并规则见GET /v1/common/symbols）。合并深度仅改变显示方式，不改变实际成交价。
        :return:
                data:
                    "tick": {
                        "bids": [
                        [买1价,买1量]
                        [买2价,买2量]
                        //more data here
                        ]
                        "asks": [
                        [卖1价,卖1量]
                        [卖2价,卖2量]
                        //more data here
                        ]
                    }
        """
        channel = """{"req": "market.%s.depth.%s","id": "id1"}""" % (symbol, type)
        print(f'channel :{channel}')
        self.send_sub(channel)
        self.recv()

    # 订阅trade
    def sub_trade_detail(self, symbol: str):
        """

        :param symbol: 交易对：btcusdt, ethusdt, ltcusdt, etcusdt, bchusdt, ethbtc, ltcbtc, etcbtc, bchbtc
        :return:
            "data": [
                {
                  "id":        消息ID,
                  "price":     成交价,
                  "time":      成交时间,
                  "amount":    成交量,
                  "direction": 成交方向,
                  "tradeId":   成交ID,
                  "ts":        时间戳
                }
            ]
        """
        channel = """{"sub": "market.%s.trade.detail","id": "id1"}""" % symbol
        print(f'channel :{channel}')
        self.send_sub(channel)
        self.recv()

    # 请求trade
    def req_trade_detail(self, symbol: str):
        """最近300个交易信息

        :param symbol: 交易对：btcusdt, ethusdt, ltcusdt, etcusdt, bchusdt, ethbtc, ltcbtc, etcbtc, bchbtc
        :return:
            "data": [
                {
                  "id":        消息ID,
                  "price":     成交价,
                  "time":      成交时间,
                  "amount":    成交量,
                  "direction": 成交方向,
                  "tradeId":   成交ID,
                  "ts":        时间戳
                }
            ]
        """
        channel = """{"req": "market.%s.trade.detail","id": "id1"}""" % symbol
        print(f'channel :{channel}')
        self.send_sub(channel)
        self.recv()

    # 请求市场详情
    def req_market_detail(self, symbol):
        """

        :param symbol: 交易对：btcusdt, ethusdt, ltcusdt, etcusdt, bchusdt, ethbtc, ltcbtc, etcbtc, bchbtc
        :return:

        """
        channel = """{"req": "market.%s.detail","id": "id12"}""" % symbol
        print(f'channel :{channel}')
        self.send_sub(channel)
        self.recv()

    # 订阅account
    def sub_accounts(self, topic: str):
        """
        :param topic: 订阅主题名称
        :return:
        """
        cid = uuid.uuid4().hex
        channel = """{"op": "sub","cid": %s,"topic": %s}""" % (cid, topic)
        # channel = """{"op": "sub","cid": "40sG903yz80oDFWr","topic": "accounts"}"""
        print(f'channel :{channel}')
        self.send_sub(channel)
        self.recv()

    # 订阅订单更新
    def sub_orders(self, symbol: str):
        """

        :param symbol: 交易对
        :return:
        """
        cid = uuid.uuid4().hex
        channel = """{"op": "sub","cid": %s,"topic": "orders.%s"}""" % (cid, symbol)
        print(f'channel :{channel}')
        self.send_sub(channel)
        self.recv()

    # 取消订阅
    def unsub_topic(self, topic: str):
        """
        :param topic:
        :return:
        """
        channel = """{"op": "unsub","topic": %s,"cid": "id11",}""" % topic
        print(f'channel :{channel}')
        self.un_sub(channel)
        self.recv()


if __name__ == "__main__":

    c = HuoBiClient()
    # c.sub_kline('btcusdt', '1min')
    # c.req_kline('btcusdt', '1min')
    # c.sub_market_depth('btcusdt', 'step0')
    # c.sub_trade_detail('btcusdt')
    # c.req_trade_detail('btcusdt')
    # c.req_market_detail('btcusdt')
    # c.sub_accounts('accounts')
    # c.sub_orders('btcusdt')
    c.unsub_topic('foo.bar')

    # while 1:
    #     try:
    #         ws = create_connection("wss://api.huobipro.com/ws")
    #         break
    #     except:
    #         print('connect ws error,retry...')
    #         time.sleep(5)
    #
    # # 订阅 KLine 数据
    # tradeStr = """{"sub": "market.ethusdt.kline.1min","id": "id10"}"""
    #
    # ws.send(tradeStr)
    # while 1:
    #     compressData = ws.recv()
    #     print(f'websocket msg:{compressData}')
    #     result = gzip.decompress(compressData).decode('utf-8')
    #     if result[:7] == '{"ping"':
    #         ts = result[8:21]
    #         pong = '{"pong":'+ts+'}'
    #         ws.send(pong)
    #         # ws.send(tradeStr)
    #     else:
    #         print(result)
