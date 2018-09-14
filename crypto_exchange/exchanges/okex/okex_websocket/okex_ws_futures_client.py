# -*- coding: utf-8 -*-
import asyncio
import hashlib
import json
import aiohttp
import datetime

API_KEY = "3b773537-bbae-4db9-9a9b-42069d7e1fbb"
SECRET_KEY = "EFAABB4F616059E45557329A86D2B77C"


class OkexFuturesWebSocketClient(object):

    def __init__(self, api_key=None, secret_key=None):
        self.url = "wss://real.okex.com:10440/websocket/okexapi"
        self.evt_ping = "{'event':'ping'}"
        self.api_key = api_key or API_KEY
        self.secret_key = secret_key or SECRET_KEY
        self.coin_types = ['btc', 'ltc', 'eth', 'etc', 'bch', 'eos', 'xrp', 'btg']
        self.durations = ['this_week', 'next_week', 'quarter']
        self.periods = ['1min', '3min', '5min', '15min', '30min', '1hour', '2hour',
                        '4hour', '6hour', '12hour', 'day', '3day', 'week']
        self.depth_size = [5, 10, 20]

    # ping
    @staticmethod
    async def timer(ws, params):
        """
        :param ws:
        :param params:
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

    # 合约行情数据
    async def futures_ticker(self, coin_type: str, duration: str):
        """
        :param coin_type: 币种 btc, ltc, eth, etc, bch, eos, xrp, btg
        :param duration: 时间区间 this_week, next_week, quarter
        :return:
            data:
                limitHigh(string):最高买入限制价格
                limitLow(string):最低卖出限制价格
                vol(double):24小时成交量
                sell(double):卖一价格
                buy(double): 买一价格
                unitAmount(double):合约价值
                hold_amount(double):当前持仓量
                contractId(long):合约ID
                high(double):24小时最高价格
                low(double):24小时最低价格
        """

        if not (coin_type in self.coin_types and duration in self.durations):
            print("params error!")
            # todo 参数错误处理
            pass
        event = "{'event':'addChannel','channel':'ok_sub_futureusd_%s_ticker_%s'}" % (coin_type, duration)
        print(f'event:{event}')
        task = self.subscribe(channel=event)
        return await task

    # 合约kline
    async def futures_kline(self, coin_type: str, duration: str, period: str):
        """
        :param coin_type: 币种 btc, ltc, eth, etc, bch, eos, xrp, btg
        :param duration: 时间区间 this_week, next_week, quarter
        :param period: 周期 1min, 3min, 5min, 15min, 30min, 1hour, 2hour, 4hour, 6hour, 12hour, day, 3day, week
        :return:
            data:
                [时间 ,开盘价,最高价,最低价,收盘价,成交量(张),成交量(币)]
        """
        if not (coin_type in self.coin_types and duration in self.durations and period in self.periods):
            print("params error!")
            # todo 参数错误处理
            pass
        event = "{'event':'addChannel','channel':'ok_sub_futureusd_%s_kline_%s_%s'}" % (coin_type, duration, period)
        print(f'event:{event}')
        task = self.subscribe(channel=event)
        return await task

    # 合约市场深度
    async def futures_depth(self, coin_type: str, duration: str):
        """
        :param coin_type: 币种 btc, ltc, eth, etc, bch, eos, xrp, btg
        :param duration: 时间区间 this_week, next_week, quarter
        :return:
            data:
                timestamp(long): 服务器时间戳
                asks(array):卖单深度 数组索引(string) 0 价格, 1 量(张), 2 量(币) 3, 累计量(币)
                bids(array):买单深度 数组索引(string) 0 价格, 1 量(张), 2 量(币) 3, 累计量(币)
                使用描述:
                    1，第一次返回全量数据
                    2，根据接下来数据对第一次返回数据进行，如下操作
                    删除（量为0时）
                    修改（价格相同量不同）
                    增加（价格不存在）
        """
        if not (coin_type in self.coin_types and duration in self.durations):
            print("params error")
            # todo 参数错误处理
            pass
        event = "{'event':'addChannel','channel':'ok_sub_futureusd_%s_depth_%s'}" % (coin_type, duration)
        print(f'event:{event}')
        task = self.subscribe(channel=event)
        return await task

    # 合约市场深度(全量返回)
    async def futures_depth_size(self, coin_type: str, duration: str, size: int):
        """
        :param coin_type: 币种 btc, ltc, eth, etc, bch, eos, xrp, btg
        :param duration: 时间区间 this_week, next_week, quarter
        :param size: 深度条数 5, 10, 20
        :return:
            data:
                timestamp(long): 服务器时间戳
                asks(array):卖单深度 数组索引(string) [价格, 量(张), 量(币),累计量(币)]
                bids(array):买单深度 数组索引(string) [价格, 量(张), 量(币),累计量(币)]
        """
        if not (coin_type in self.coin_types and duration in self.durations and size in self.depth_size):
            print("params error")
            # todo 参数错误处理
            pass
        event = "{'event':'addChannel','channel':'ok_sub_futureusd_%s_depth_%s_%s'}" % (coin_type, duration, size)
        print(f'event:{event}')
        task = self.subscribe(channel=event)
        return await task

    # 合约交易信息
    async def futures_trade(self, coin_type: str, duration: str):
        """
        :param coin_type: 币种 btc, ltc, eth, etc, bch, eos, xrp, btg
        :param duration: 时间区间 this_week, next_week, quarter
        :return:
            data:
                [交易序号, 价格, 成交量(张), 时间, 买卖类型，成交量(币-新增)]
                [string, string, string, string, string, string]
        """
        if not (coin_type in self.coin_types and duration in self.durations):
            print("params error")
            # todo 参数错误处理
            pass
        event = "{'event':'addChannel','channel':'ok_sub_futureusd_%s_trade_%s'}" % (coin_type, duration)
        print(f'event:{event}')
        task = self.subscribe(channel=event)
        return await task

    # 合约指数
    async def futures_index(self, coin_type):
        """
        :param coin_type: 币种 btc, ltc, eth, etc, bch, eos, xrp, btg
        :return:
            data:
                futureIndex(string): 指数
                timestamp(string): 时间戳
        """
        if not (coin_type in self.coin_types):
            print("params error")
            # todo 参数错误处理
            pass

        event = "{'event':'addChannel','channel':'ok_sub_futureusd_%s_index'}" % coin_type
        print(f'event:{event}')
        task = self.subscribe(channel=event)
        return await task

    # 合约预估交割价格
    async def futures_forecast_price(self, coin_type: str):
        """
        :param coin_type: 币种 btc, ltc, eth, etc, bch, eos, xrp, btg
        :return:
            data(string): 预估交割价格
            timestamp(string): 时间戳
            操作说明
            无需订阅，交割前一小时自动返回
        """
        if coin_type not in self.coin_types:
            print("params error")
            # todo 参数错误处理
            pass
        event = "{'event':'addChannel','channel':'%s_forecast_price'}" % coin_type
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

    # 登录事件
    async def login(self):
        sign = self.sign(params={'api_key': self.api_key}, secret_key=self.secret_key)

        params = {"event": "login",
                  "parameters": {"api_key": self.api_key, "sign": sign}}

        trade_params = {"event": "addChannel",
                        "channel": "ok_sub_futureusd_trades",
                        "parameters": {"api_key": self.api_key, "sign": sign}}
        session = aiohttp.ClientSession()
        async with session.ws_connect(url=self.url) as ws:
            # 登录
            await ws.send_json(data=params)
            msg = await ws.receive()
            result = json.loads(msg.data)
            print(f"login result: {result}")
            if not result[0].get('data').get('result'):
                # 登录失败
                # todo 登录失败处理
                pass

    # 个人合约交易信息
    async def futureusd_trades(self):
        sign = self.sign(params={'api_key': self.api_key}, secret_key=self.secret_key)
        trade_params = {"event": "trades",
                        "channel": "ok_sub_futureusd_trades",
                        "parameters": {"api_key": self.api_key, "sign": sign}}
        session = aiohttp.ClientSession()
        async with session.ws_connect(url=self.url) as ws:
            # 交易
            await ws.send_json(data=trade_params)
            msg = await ws.receive()
            result = json.loads(msg.data)
            print(f"trade result: {result}")


    # 个人合约账户信息
    async def futureusd_userinfo(self):
        pass

    # 合约持仓信息
    async def futureusd_positions(self):
        pass


if __name__ == '__main__':
    print('Type "exit" to quit')
    loop = asyncio.get_event_loop()
    c = OkexFuturesWebSocketClient()
    # task = c.futures_ticker(coin_type="btc", duration="this_week")
    # task = c.futures_depth(coin_type="btc", duration='this_week')
    # task = c.futures_depth_size(coin_type="btc", duration='this_week', size=5)
    # task = c.futures_trade(coin_type="btc", duration='this_week')
    # task = c.futures_kline(coin_type="btc", duration='this_week', period="1min")
    # task = c.futures_index(coin_type="btc")
    # task = c.futures_forecast_price(coin_type="btc")
    # task = c.login()
    task = c.futureusd_trades()
    # task = c.spot_balance(symbol="bch_btc")
    loop.run_until_complete(task)

