from pprint import pprint
import pytest
from crypto_exchange.exchanges.huobi.huobi_websocket.huobi_ws_client import huobi_k_line
import logging
logger = logging.getLogger(__name__)


def test_k_line():
    data = huobi_k_line()
    for i in data:
        pprint(i)
