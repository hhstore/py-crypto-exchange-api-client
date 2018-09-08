
from crypto_exchange.exchanges.huobi.huobi_websocket.huobi_ws_client import huobi


def huobi_unsub_k_line():
    huobi.un_sub(""" {
  "unsub": "market.btcusdt.kline.1min",
  "id": "id1"
}""")


huobi_unsub_k_line()
