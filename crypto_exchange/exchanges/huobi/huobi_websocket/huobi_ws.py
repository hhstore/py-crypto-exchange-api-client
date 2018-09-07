import gzip
import json
import logging
import time
from pprint import pprint

from websocket import create_connection

logger = logging.getLogger(__name__)


class HuoBi(object):

    def __init__(self):
        self.url = "wss://api.huobipro.com/ws"
        self.ws = None
        self.data = None


        while True:
            try:
                self.ws = create_connection(self.url)
                break
            except Exception as e:
                logger.error(e)
                print('connect ws error,retry...')
                time.sleep(5)

    def send(self, data):
        self.data = data
        self.ws.send(data)

    def recv(self):
        while True:
            compress_data = self.ws.recv()
            result = gzip.decompress(compress_data).decode('utf-8')

            if result[:7] == '{"ping"':
                ts = result[8:21]
                pong = '{"pong":' + ts + '}'
                self.ws.send(pong)
                self.ws.send(self.data)
            else:
                result = json.loads(result)
                print(result)


