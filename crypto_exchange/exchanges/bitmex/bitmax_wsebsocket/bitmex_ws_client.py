# -*- coding: utf-8 -*-
import asyncio
import gzip
import json
from datetime import datetime
from collections import defaultdict
import aiohttp
import logging


log = logging.getLogger(__name__)


class BitmexWsClient:

    def __init__(self, data_parser, url=None, api_key=None, secret_key=None,):
        """
        :param data_parser: 数据转换函数
        :param url: ws 连接url
        :param api_key: api key
        :param secret_key:  secret key
        """

        self.api_key = api_key
        self.secret_key = secret_key

        self.url = url or 'wss://www.bitmex.com/realtime'
        self.data_parser = data_parser
        # ws client session
        self.session = None
        self.ws = None
        # ws is connected
        self.connected = False

        self.ensure_connection = True
        self.pong = 0
        self.lock = asyncio.Lock()
        # sub data handle
        self.queue_handlers = defaultdict(list)
        self.data_queue = {}
        # task list
        self.task_list = []
        self.task_list.append(asyncio.ensure_future(self.ensure_connected()))
        self.task_list.append(asyncio.ensure_future(self.ping()))

    async def ensure_connected(self):
        print(f"Connecting to {self.url}")
        sleep_seconds = 2
        while self.ensure_connection:
            # 未连接
            if not self.connected:
                try:
                    # 创建session
                    self.session = aiohttp.ClientSession()
                    self.ws = await self.session.ws_connect(self.url, autoping=True, timeout=30)
                except Exception as e:
                    try:
                        await self.session.close()
                    except:
                        print('close session fail')
                        log.exception('close session fail')
                    self.session = None
                    self.ws = None
                    print(f'try connect to {self.url} failed, sleep for {sleep_seconds} seconds...', e)
                    log.warning(f'try connect to {self.url} failed, sleep for {sleep_seconds} seconds...', e)
                    await asyncio.sleep(sleep_seconds)
                    sleep_seconds = min(sleep_seconds * 2, 64)
                else:
                    print('Connected to WS')
                    log.debug('Connected to WS')
                    self.connected = True
                    sleep_seconds = 2
                    self.pong = datetime.utcnow().timestamp()
                    asyncio.ensure_future(self.on_msg())

                    # 重新连接需要重新订阅queue里已经订阅的数据
                    async with self.lock:
                        # 获取去重的所有q_key
                        q_keys = list(self.queue_handlers.keys())
                        if q_keys:
                            print('recover subscriptions: {}'.format(q_keys))
                            for q_key in q_keys:
                                sub_data = json.loads(q_key)
                                asyncio.ensure_future(self.subscribe_data(**sub_data))
            else:
                await asyncio.sleep(1)

    # ping
    async def ping(self):
        while True:
            try:
                if self.ws and not self.ws.closed:
                    if datetime.now().timestamp() - self.pong > 20:
                        print('connection heart beat lost')
                        await self.ws.close()
                    else:
                        # todo ping数据需要修改
                        await self.ws.send_json({'op': 'ping'})
            finally:
                # 5秒间隔
                await asyncio.sleep(5)

    # 接收消息
    async def on_msg(self):
        while not self.ws.closed:
            msg = await self.ws.receive()
            try:
                if msg.type == aiohttp.WSMsgType.TEXT:
                    data = json.loads(msg.data)
                    await self.handle_message(data)
                elif msg.type == aiohttp.WSMsgType.BINARY:
                    data = json.loads(gzip.decompress(msg.data).decode())
                    await self.handle_message(data)
                elif msg.type == aiohttp.WSMsgType.CLOSED:
                    print('ws closed')
                    break
                elif msg.type == aiohttp.WSMsgType.ERROR:
                    print('ws error', msg)
                    break
            except Exception as e:
                print('msg error...', e)

        try:
            await self.ws.close()
        except:
            pass

        self.connected = False
        print('ws was disconnected...')
        log.warning('ws was disconnected...')

    # 处理消息
    async def handle_message(self, data):
        print(f"receive msg{data}")
        try:
            if 'error' in data:
                print(f"error msg:{data.get('error')}")
                log.warning(f"error msg:{data.get('error')}")
                return
            # 订阅成功消息处理
            if 'subscribe' in data:
                if 'success' in data:
                    is_ok = data.get('success')
                    # todo 判断是否消息code码
                    if is_ok:
                        print('sub sucess')
                        log.debug('sub success')
                    else:
                        log.warning('sub failed')

                else:
                    print('unexpected msg get', data)
                return
            op = data.get('op')
            # pong消息处理
            if op == 'pong':
                self.pong = datetime.now().timestamp()
                return

            # todo 订阅channel消息处理
            q_key, parsed_data = self.data_parser(data)
            if q_key is None:
                log.warning('unknown msg:{}'.format(data))
                print('unknown msg:{}'.format(data))
                return
            if q_key in self.data_queue:
                # 数据放入asyncio.Queue中
                self.data_queue.get(q_key).put_nowait(parsed_data)
        except Exception as e:
            print('unexpected msg format', data, e)
            log.warning('unexpected msg format', data, e)

    # close
    async def close(self):
        self.ensure_connection = False
        for task in self.task_list:
            task.cancel()
        if self.session:
            await self.session.close()

    # 订阅数据
    async def subscribe_data(self, uri: str, on_update=None):
        print(f'subscribe: {uri}')
        while not self.connected:
            await asyncio.sleep(1)

        # 请求数据
        sub_data = {"op": "subscribe", "args": uri}
        # 数据排序（可免）
        q_key = json.dumps(sub_data, sort_keys=True)
        async with self.lock:
            try:
                await self.ws.send_json(sub_data)
                print(f'sub data:{sub_data}')
                # 订阅数据不在queue中
                if q_key not in self.data_queue:
                    self.data_queue[q_key] = asyncio.Queue()
                    # 有更新且处理器列表不为空，数据更新，回调函数重新执行
                    if on_update and not self.queue_handlers.get(q_key):
                        asyncio.ensure_future(self.handle_q(q_key))
            except Exception as e:
                print(f'subscribe {sub_data} failed!', e)
            else:
                if on_update:
                    self.queue_handlers[q_key].append(on_update)

    async def handle_q(self, q_key):
        while q_key in self.data_queue:
            q = self.data_queue.get(q_key)
            try:
                # asyncio.Queue中获取数据
                tk = await q.get()
            except:
                print('get data from queue failed:{}'.format(q_key))
                continue
            # 回调函数回调数据
            for callback in self.queue_handlers.get(q_key):
                if asyncio.iscoroutinefunction(callback):
                    await callback(tk)
                else:
                    callback(tk)


class OrderBookL2(BitmexWsClient):

    def __init__(self, key, channel):
        super().__init__(data_parser=self.parse_data, api_key=key)
        self.channel = channel

    def parse_data(self, data):
        print('parse data:{}'.format(data))
        q_key = json.dumps({'op': 'subscribe', 'args': self.channel}, sort_keys=True)
        return q_key, data

    async def subscribe_orderbook(self, on_update=None):
        await self.subscribe_data(uri=self.channel, on_update=on_update)




_client_pool = {}


async def get_client(key='default'):
    if key in _client_pool:
        return _client_pool.get(key)
    else:
        c = OrderBookL2(key)
        _client_pool[key] = c
        return c


async def subscribe_orderbook():
    c = OrderBookL2(key='default', channel="orderBookL2:BTCUSDT")
    return await c.subscribe_orderbook(on_update=True)




    # # kline
    # async def kline(self, symbol: str, period: str):
    #     """
    #     :param symbol: 交易对：大写
    #     :param period: 周期：1m, 5m, 1h, 1d
    #     :return:
    #     """
    #     channel = "quoteBin%s:%s" % (period, symbol.upper())
    #     if channel not in self.sub_queue:
    #         self.sub_queue[channel] = {}
    #     if self.ws_state == READY:
    #         await self.ws.send_json({'op': 'subscribe', "args": channel})
    #     elif self.ws_state == IDLE:
    #         self.set_ws_state(GOING_TO_CONNECT, 'user sub order')


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    task = subscribe_orderbook()
    loop.run_until_complete(task)
