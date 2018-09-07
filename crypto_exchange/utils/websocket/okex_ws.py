# Import Built-Ins
import json
import threading
import time
from pprint import pprint

import aiohttp
import hashlib
import logging

# Import Third-Party

# Import Homebrew
from websocket import create_connection, WebSocketTimeoutException

from crypto_exchange.utils.websocket.api_ws import WSSAPI

log = logging.getLogger(__name__)
URL = "wss://real.okex.com:10441/websocket"
API_KEY = "3b773537-bbae-4db9-9a9b-42069d7e1fbb"
SECRET_KEY = "EFAABB4F616059E45557329A86D2B77C"


# Import Built-Ins
import logging
import json
import threading
import time

# Import Third-Party
from websocket import create_connection, WebSocketTimeoutException
import requests

# Import Homebrew


# Init Logging Facilities
log = logging.getLogger(__name__)


class OKCoinWSS(WSSAPI):
    def __init__(self):
        super(OKCoinWSS, self).__init__('wss://real.okcoin.com:10440/websocket/okcoinapi ',
                                        'OKCoin')
        self.conn = None

        self.pairs = 'bch_btc'
        self._data_thread = None

    def start(self):
        super(OKCoinWSS, self).start()

        self._data_thread = threading.Thread(target=self._process_data)
        self._data_thread.daemon = True
        self._data_thread.start()

    def stop(self):
        super(OKCoinWSS, self).stop()

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

ok=OKCoinWSS()
ok.start()
