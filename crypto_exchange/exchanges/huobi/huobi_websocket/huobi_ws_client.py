# -*- coding: utf-8 -*-
import asyncio
import json
import gzip
from datetime import datetime
import aiohttp

# websocket status
IDLE = 'idle'
GOING_TO_CONNECT = 'going-to-connect'
CONNECTING = 'connecting'
READY = 'ready'
GOING_TO_DICCONNECT = 'going-to-disconnect'
API_KEY = ''
SECRET_KEY = ''


class HuobiWebSocketClient(object):

    def __init__(self, api_key=None, secret_key=None, loop=None):
        """
        :param api_key:
        :param secret_key:
        """
        self.url = "wss://api.huobipro.com/ws"
        self.api_key = api_key or API_KEY
        self.secret_key = secret_key or SECRET_KEY

        self.session = aiohttp.ClientSession(loop=loop)
        self.ws = None
        self.ws_state = GOING_TO_CONNECT
        self.ws_support = True
        self.last_pong = 0
        self.closed = False

        self.sub_queue = {}
        # asyncio.ensure_future(self.keep_connection())

    @property
    def is_running(self):
        return not self.closed

    # close
    def close(self):
        if self.ws and not self.ws.closed:
            asyncio.ensure_future(self.ws.close())
        if self.session and not self.session.closed:
            asyncio.ensure_future(self.session.close())
        self.closed = True

    # set ws status
    def set_ws_state(self, new, reason=''):
        print(f'set ws state from {self.ws_state} to {new}', reason)
        self.ws_state = new

    # keep connection
    async def keep_connection(self):
        while self.is_running:
            if not self.ws_support:
                break
            if self.ws_state == GOING_TO_CONNECT:
                await self.ws_connect()
            elif self.ws_state == READY:
                try:
                    while not self.ws.closed:
                        ping = datetime.now().timestamp()
                        await self.ws.send_str("{'ping': %s}" % 18212558000)
                        await asyncio.sleep(10)
                        if self.last_pong < ping:
                            print('ws connection heartbeat lost')
                            break
                except:
                    print('ws connection ping failed')
                finally:
                    self.set_ws_state(GOING_TO_CONNECT, 'heartbeat lost')
            elif self.ws_state == GOING_TO_DICCONNECT:
                await self.ws.close()
            await asyncio.sleep(5)

    # websocket connect
    async def ws_connect(self):
        self.set_ws_state(CONNECTING)
        try:
            print(self.url)
            self.ws = await self.session.ws_connect(self.url, timeout=30)
        except:
            self.set_ws_state(GOING_TO_CONNECT, 'ws connect failed')
            print('ws connect failed')
            await asyncio.sleep(5)
        else:
            print('ws connected.')
            asyncio.ensure_future(self.on_msg())

    # read msg
    async def on_msg(self, ws, channel):
        while not ws.closed:
            msg = await ws.receive()
            print("websocket result:{}".format(msg))
            try:
                if msg.type == aiohttp.WSMsgType.TEXT:
                    await self.handle_message(msg.data)
                elif msg.type == aiohttp.WSMsgType.BINARY:
                    data = json.loads(gzip.decompress(msg.data).decode())
                    # 响应websocket server ping 保持连接
                    if isinstance(msg, dict) and 'ping' in msg.keys():
                        await ws.send_json({"pong": msg.get("ping")})
                    else:
                        # 正常处理消息
                        await self.handle_message(data)
                elif msg.type == aiohttp.WSMsgType.CLOSED:
                    print('closed')
                    break
                elif msg.type == aiohttp.WSMsgType.ERROR:
                    print('error', msg)
                    break
            except Exception as e:
                print('msg error...', e)
            await ws.send_str(data=channel)
        self.set_ws_state(GOING_TO_CONNECT, 'ws was disconnected...')

    # handle msg
    async def handle_message(self, msg):
        print(f'msg data:{msg}')

    # 订阅 KLine 数据
    async def kline(self, symbol: str, period: str):
        """
        :param symbol: 交易对：ethbtc, ltcbtc, etcbtc, bchbtc等
        :param period: 周期：1min, 5min, 15min, 30min, 60min, 1day, 1mon, 1week, 1year
        :return:
        """
        channel = "{'sub': 'market.%s.kline.%s', 'id': 'id1'}" % (symbol, period)
        channel = """{"sub": "market.ethusdt.kline.1min","id": "id10"}"""
        session = aiohttp.ClientSession()
        async with session.ws_connect(url=self.url, autoping=False) as ws:
            # 发送订阅数据
            print('channel:{}'.format(channel))
            ws.send_str(data=channel)
            while 1:
                compressData = await ws.receive()
                print(f'websocket msg:{compressData}')
                result = gzip.decompress(compressData.data).decode()
                if result[:7] == '{"ping"':
                    ts = result[8:21]
                    pong = '{"pong":' + ts + '}'
                    ws.send_json(pong)
                    ws.send_str(data=channel)
                else:
                    print(result)

            # await self.on_msg(ws=ws, channel=channel)

    async def read_msg(self, ws, channel: str):
        start_timestamp = datetime.utcnow().timestamp()
        async for msg in ws:
            print('start:{}'.format(int(start_timestamp)))
            if msg.type in (aiohttp.WSMsgType.CLOSED, aiohttp.WSMsgType.ERROR):
                print("websocket closed or msg type error")
                # todo raise exception?
                ws.close()
                raise aiohttp.ServerDisconnectedError(message='closed')

            print(f"ws msg:{msg}")
            # todo 消息处理
            data = json.loads(gzip.decompress(msg.data).decode())
            if 'ping' in data.keys():
                await ws.send_json({"pong": data.get("ping")})
                await ws.send_str(data=channel)
            print(f"data: {data}")


if __name__ == '__main__':
    print('Type "exit" to quit')
    loop = asyncio.get_event_loop()
    c = HuobiWebSocketClient(loop=loop)
    task = c.kline(symbol="bchbtc", period="1min")
    # loop.run_forever()

    loop.run_until_complete(task)


# def huobi_k_line(symbol: str, period: str):
#     """
#     订阅 KLine 数据
#     :param symbol btcusdt, ethusdt, ltcusdt, etcusdt, bchusdt, ethbtc, ltcbtc, etcbtc, bchbtc...
#     :param period 1min, 5min, 15min, 30min, 60min, 1day, 1mon, 1week, 1year
#     :return:
#     """
#     huobi = HuoBi()
#     huobi.send_sub("""{"sub": "market.%s.kline.%s","id": "id1"}""" % (symbol, period))
#     yield from huobi.recv()
#
#
# def huobi_req_k_line(symbol: str, period: str):
#     """
#     请求 KLine 数据
#     :param symbol btcusdt, ethusdt, ltcusdt, etcusdt, bchusdt, ethbtc, ltcbtc, etcbtc, bchbtc...
#     :param period 1min, 5min, 15min, 30min, 60min, 1day, 1mon, 1week, 1year
#     :return:
#     """
#     huobi = HuoBi()
#     huobi.send_sub("""{"req": "market.%s.kline.%s","id": "id1"}""" % (symbol, period))
#     yield from huobi.recv()
#
#
# def huobi_depth(symbol: str, depth_type: str):
#     """
#     订阅 Market Depth 数据
#     :param symbol: btcusdt, ethusdt, ltcusdt, etcusdt, bchusdt, ethbtc, ltcbtc, etcbtc, bchbtc...
#     :param depth_type: step0, step1, step2, step3, step4, step5（合并深度0-5）；step0时，不合并深度
#     :return:
#     """
#     huobi = HuoBi()
#     huobi.send_sub("""{"sub": "market.%s.depth.%s","id": "id1"}""" % (symbol, depth_type))
#     yield from huobi.recv()
#
#
# def huobi_trade_detail(symbol: str):
#     """
#     订阅 Trade Detail 数据
#     :param symbol:
#     :return:
#     """
#     huobi = HuoBi()
#     huobi.send_sub("""{"sub": "market.%s.trade.detail","id": "id1"}""" % symbol)
#     yield from huobi.recv()
#
#
# def huobi_detail(symbol: str):
#     """
#     请求 Market Detail 数据
#     :param symbol:
#     :return:
#     """
#     huobi = HuoBi()
#     huobi.send_sub("""{"sub": "market.%s.detail","id": "id1"}""" % symbol)
#     yield from huobi.recv()


# 订阅 KLine 数据
# data = huobi_k_line('ethbtc', '1min')

# 订阅 Market Depth 数据
# data = huobi_depth('ethbtc', 'step1')

# 订阅 Trade Detail 数据
# data = huobi_trade_detail('ethbtc')

# 请求 Market Detail 数据
# data = huobi_detail('ethbtc')

