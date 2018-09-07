import logging
from pprint import pprint

from crypto_exchange.exchanges.huobi.huobi_websocket.huobi_ws import HuoBi

logger = logging.getLogger(__name__)


def huobi_k_line():
    huobi=HuoBi()
    huobi.send(""" {
  "sub": "market.btcusdt.kline.1min",
  "id": "id1"
}""")
    data=huobi.recv()
    pprint(data)

huobi_k_line()
