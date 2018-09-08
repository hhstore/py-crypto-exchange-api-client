import gzip
import json
import logging
import time
from pprint import pprint
from queue import Queue

from websocket import create_connection

logger = logging.getLogger(__name__)


class HuoBi(object):

    def __init__(self):
        self.url = "wss://api.huobipro.com/ws"
        self.ws = None
        self.data = None
        self.queue = Queue()

        try:
            self.ws = create_connection(self.url)

        except Exception as e:
            logger.error(e)
            print('connect ws error,retry...')
            time.sleep(5)

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
        while True:
            compress_data = self.ws.recv()
            result = gzip.decompress(compress_data).decode('utf-8')

            if result[:7] == '{"ping"':
                ts = result[8:21]
                pong = '{"pong":' + ts + '}'
                self.ws.send(pong)
                pprint('发送pong')
                # self.ws.send(self.data)
            else:
                result = json.loads(result)
                yield result

    def un_sub(self, un_sub_data):
        # un_sub_data = re.sub(r'sub', 'unsub', self.data)
        pprint(un_sub_data)
        self.ws.send(un_sub_data)
        pprint('取消订阅')
