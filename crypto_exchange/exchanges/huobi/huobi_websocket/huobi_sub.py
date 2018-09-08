from pprint import pprint

from crypto_exchange.exchanges.huobi.huobi_websocket.huobi_ws_client import huobi


def huobi_k_line():

    huobi.send_sub(""" {
  "sub": "market.btcusdt.kline.1min",
  "id": "id1"
}""")
    huobi.recv()
    return huobi.data()

data = huobi_k_line()
pprint(data)
