import gzip
import hashlib
import json
import time
import logging
from pprint import pprint

from websocket import create_connection

logger = logging.getLogger(__name__)


class OKEx(object):

    def __init__(self, url="wss://real.okex.com:10441/websocket"):
        self.url = url
        self.ws = None
        self.data = None

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
            result = compress_data
            # pprint(result)
            if result[:7] == '{"ping"':
                ts = result[8:21]
                pong = '{"pong":' + ts + '}'
                self.ws.send(pong)
                pprint('发送pong')
                # self.ws.send(self.data)
            else:
                result = json.loads(result)
                yield result

    def sign(self, params: dict, secret_key):
        sign = ''
        # 对参数进行排序,拼接数据
        for key in sorted(params.keys()):
            sign += key + "=" + str(params[key]) + "&"
        data = sign + "secret_key=" + secret_key
        # 签名
        return hashlib.md5(data.encode("utf8")).hexdigest().upper()
