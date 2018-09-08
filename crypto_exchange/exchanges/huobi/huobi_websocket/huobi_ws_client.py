import logging
import time
from pprint import pprint

from crypto_exchange.exchanges.huobi.huobi_websocket.huobi_ws import HuoBi

logger = logging.getLogger(__name__)


def huobi_k_line():
    """
    订阅 KLine 数据 market.$symbol.kline.$period
    :return:
    """
    huobi = HuoBi()
    huobi.send_sub(""" {
  "sub": "market.btcusdt.kline.1min",
  "id": "id1"
}""")

    yield from huobi.recv()


data = huobi_k_line()
for i in data:
    pprint(i)

