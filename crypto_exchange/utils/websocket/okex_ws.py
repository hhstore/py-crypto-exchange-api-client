# Import Built-Ins
import json
import threading
import time

import aiohttp
import hashlib
import logging

# Import Third-Party

# Import Homebrew
from websocket import create_connection, WebSocketTimeoutException

from crypto_exchange.utils.websocket.api_ws import WSSAPI

log = logging.getLogger(__name__)


class OKexWSS(WSSAPI):
    def __init__(self, url, api_key, secret_key):
        super(OKexWSS, self).__init__(url, api_key, secret_key)

        # self.conn = None
        # self.pairs = ['BTC', 'LTC']
        # self._data_thread = None

    def sign(self, params: dict, method: str = None, host_url: str = None, end_url: str = None):
        sign = ''
        # 对参数进行排序,拼接数据
        for key in sorted(params.keys()):
            sign += key + "=" + str(params[key]) + "&"
        data = sign + "secret_key=" + self.secret_key
        # 签名
        return hashlib.md5(data.encode("utf8")).hexdigest().upper()

    def start(self):
        super(OKexWSS, self).start()

        self._data_thread = threading.Thread(target=self._process_data)
        self._data_thread.daemon = True
        self._data_thread.start()

    def stop(self):
        super(OKexWSS, self).stop()

        self._data_thread.join()

    def _process_data(self):
        self.conn = create_connection(self.addr, timeout=4)
        for pair in self.pairs:
            payload = [{'event': 'addChannel',
                        'channel': 'ok_sub_spotusd_%s_ticker' % pair},
                       {'event': 'addChannel',
                        'channel': 'ok_sub_spotusd_%s_depth_60' % pair},
                       {'event': 'addChannel',
                        'channel': 'ok_sub_spotusd_%s_trades' % pair},
                       {'event': 'addChannel',
                        'channel': 'ok_sub_spotusd_%s_kline_1min' % pair}]
            log.debug(payload)
            self.conn.send(json.dumps(payload))
        while self.running:
            try:
                data = json.loads(self.conn.recv())
            except (WebSocketTimeoutException, ConnectionResetError):
                self._controller_q.put('restart')

            if 'data' in data:
                pair = ''.join(data['channel'].split('spot')[1].split('_')[:2]).upper()
                self.data_q.put((data['channel'], pair, data['data'],
                                 time.time()))
            else:
                log.debug(data)
        self.conn = None
