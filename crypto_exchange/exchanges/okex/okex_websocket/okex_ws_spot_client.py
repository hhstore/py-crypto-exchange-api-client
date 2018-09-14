# -*- coding: utf-8 -*-
import asyncio
import hashlib
import json
import os
import aiohttp
import datetime

API_KEY = "3b773537-bbae-4db9-9a9b-42069d7e1fbb"
SECRET_KEY = "EFAABB4F616059E45557329A86D2B77C"


class OkexSpotWebSocketClient(object):

    def __init__(self, api_key=None, secret_key=None):
        self.url = "wss://real.okex.com:10441/websocket"
        self.evt_ping = "{'event':'ping'}"
        self.api_key = api_key or API_KEY
        self.secret_key = secret_key or SECRET_KEY

    # ping
    @staticmethod
    async def timer(ws, params):
        """

        :param ws:
        :param params:
        :param timeout:
        :return:
        """
        # ping
        await ws.send_str(params)
        msg = await ws.receive()
        print(f"pong msg: {msg}")
        # sleep
        # await asyncio.sleep(timeout)

    # 消息订阅
    async def subscribe(self, channel: str, keep_alive=True):
        """
        :param channel:
        :param keep_alive:
        :return:
        """
        session = aiohttp.ClientSession()
        async with session.ws_connect(url=self.url) as ws:
            if channel:
                await ws.send_str(channel)
            try:
                await self.read_msg(ws=ws, keep_alive=keep_alive)
            except aiohttp.ServerDisconnectedError as e:
                if e.message == 'closed':
                    # todo 重新连接
                    pass

    # read msg
    async def read_msg(self, ws, keep_alive=True):
        """
        :param ws:
        :param keep_alive:
        :return:
        """
        start_timestamp = datetime.datetime.utcnow().timestamp()
        async for msg in ws:
            print('start:{}'.format(int(start_timestamp)))
            if msg.type in (aiohttp.WSMsgType.CLOSED, aiohttp.WSMsgType.ERROR):
                print("websocket closed or msg type error")
                # todo raise exception?
                ws.close()
                raise aiohttp.ServerDisconnectedError(message='closed')

            print(f"ws msg:{msg}")
            # todo 消息处理
            data = json.loads(msg.data)
            print(f"data: {data}")

            if keep_alive:
                intervel = datetime.datetime.utcnow().timestamp() - start_timestamp
                if intervel >= 20:
                    print(f"intervel: {intervel}")
                    await self.timer(ws=ws, params=self.evt_ping)
                    start_timestamp = datetime.datetime.utcnow().timestamp()

    # 行情数据
    async def spot_ticker(self, symbol: str):
        """
        :param symbol: 交易对
        :return:
        """
        event = "{'event':'addChannel','channel':'ok_sub_spot_%s_ticker'}" % symbol
        print(f'event:{event}')

        task = self.subscribe(channel=event)
        return await task

    # 币币市场深度(200增量数据返回)
    async def spot_depth(self, symbol: str):
        """
        :param symbol: 交易对
        :return: 第一次为全量数据
        """
        event = "{'event':'addChannel','channel':'ok_sub_spot_%s_depth'}" % symbol
        print(f'event:{event}')

        task = self.subscribe(channel=event)
        return await task

    # 市场深度
    async def spot_depth_size(self, symbol: str, size: int):
        """
        :param symbol: 交易对
        :param size: 深度条数
        :return:
            msg.data
                [
                    {
                        "channel": "ok_sub_spot_bch_btc_depth_5",
                        "data": {
                            "asks": [], 买方深度
                            "bids": [], 卖方深度
                            "timestamp": 1504529432367, 服务器时间戳
                        }
                    }
                ]
        """
        event = "{'event':'addChannel','channel':'ok_sub_spot_%s_depth_%s'}" % (symbol, size)
        print(f'event:{event}')
        task = self.subscribe(channel=event)
        return await task

    # 成交记录
    async def spot_deals(self, symbol: str):
        """
        :param symbol: 交易对
        :return:
            msg.data
                [{
                    "channel":"ok_sub_spot_bch_btc_deals",
                    "data":[["1001","2463.86","0.052","16:34:07","ask"]]
                }]
                data: 交易号,价格，成交量，时间，买卖类型
        """
        event = "{'event':'addChannel','channel':'ok_sub_spot_%s_deals'}" % symbol
        print(f'event:{event}')
        task = self.subscribe(channel=event)
        return await task

    # K线数据
    async def spot_kline(self, symbol: str, period: str):
        """
        :param symbol: 交易对
        :param period: 周期
        :return:
            msg.data
                [{
                    "channel":"ok_sub_spot_bch_btc_kline_1min",
                    "data":[
                        ["1490337840000","995.37","996.75","995.36","996.75","9.112"]
                    ]
                }]
                data: [时间，开盘价，最高价，最低价，收盘价，成交量]
        """
        periods = ["1min", "3min", "5min", "15min", "30min", "1hour",
                   "2hour", "4hour", "6hour", "12hour", "day", "3day", "week"]

        event = "{'event':'addChannel','channel':'ok_sub_spot_%s_kline_%s'}" % \
                (symbol, period if period in periods else "1min")
        print(f'event:{event}')

        task = self.subscribe(channel=event)
        return await task

    @staticmethod
    def sign(params: dict, secret_key):
        """
        :param params:
        :param secret_key:
        :return:
        """
        sign = ''
        # 对参数进行排序,拼接数据
        for key in sorted(params.keys()):
            sign += key + "=" + str(params[key]) + "&"
        data = sign + "secret_key=" + secret_key
        # 签名
        return hashlib.md5(data.encode("utf8")).hexdigest().upper()

    # API用户登录
    def login(self):
        sign = self.sign(params={'api_key': self.api_key}, secret_key=self.secret_key)

        params = {"event": "login",
                  "parameters": {"api_key": self.api_key, "sign": sign}}
        return params

    # 用户交易订单
    async def spot_order(self, symbol: str):
        """
        :param symbol: 交易对
        :return:
        """
        session = aiohttp.ClientSession()
        async with session.ws_connect(url=self.url) as ws:
            # 登录
            await ws.send_json(data=self.login())
            msg = await ws.receive()
            result = json.loads(msg.data)
            print(f"login result: {result}")
            if not result[0].get('data').get('result'):
                # 登录失败
                # todo 登录失败处理
                pass
            event = {
                "event": "addChannel",
                "channel": "ok_sub_spot_%s_balance" % symbol,
                "parameters": {
                    "api_key": self.api_key,
                    "symbol": symbol,
                    "sign": self.sign(params={"symbol": symbol}, secret_key=self.secret_key)
                }
            }
            # event = "{'event':'addChannel','channel':'ok_sub_spot_%s_order'}" % symbol
            await ws.send_json(event)
            await self.timer(ws, self.evt_ping)
            try:
                await self.read_msg(ws=ws, keep_alive=True)
            except aiohttp.ServerDisconnectedError as e:
                if e.message == 'closed':
                    # todo 重新连接
                    pass

    # 用户账户信息
    async def spot_balance(self, symbol: str):
        """
        :param symbol: 交易对
        :return:
        """
        session = aiohttp.ClientSession()
        async with session.ws_connect(url=self.url) as ws:
            # 登录
            await ws.send_json(data=self.login())
            msg = await ws.receive()
            result = json.loads(msg.data)
            print(f"login result: {result}")
            if not result[0].get('data').get('result'):
                # 登录失败
                # todo 登录失败处理
                pass
            # event = "{'event':'addChannel','channel':'ok_sub_spot_%s_balance'}" % symbol
            event = {
                "event": "addChannel",
                "channel": "ok_sub_spot_%s_balance" % symbol,
                "parameters": {
                    "api_key": self.api_key,
                    "symbol": symbol,
                    "sign": self.sign(params={"symbol": symbol}, secret_key=self.secret_key)
                }
            }
            await ws.send_json(event)
            try:
                await self.read_msg(ws=ws, keep_alive=True)
            except aiohttp.ServerDisconnectedError as e:
                if e.message == 'closed':
                    # todo 重新连接
                    pass


if __name__ == '__main__':
    print('Type "exit" to quit')
    loop = asyncio.get_event_loop()
    # loop.run_until_complete(main())
    # loop.run_until_complete(exchange())

    # url = "wss://real.okex.com:10441/websocket"
    # event = "{'event':'addChannel','channel':'ok_sub_spot_X_ticker'}"
    # event = "{'event':'addChannel','channel':'ok_sub_spot_bch_btc_ticker'}"
    # ex = okex_ws(url=url, params=event)

    c = OkexSpotWebSocketClient()
    # task = c.spot_ticker(symbol="bch_btc")
    # task = c.spot_depth(symbol="bch_btc")
    # task = c.spot_depth_size(symbol="bch_btc", size=5)
    # task = c.spot_deals(symbol="bch_btc")
    # task = c.spot_kline(symbol="bch_btc", period="1min")
    task = c.spot_order(symbol="bch_btc")
    # task = c.spot_balance(symbol="bch_btc")
    loop.run_until_complete(task)
