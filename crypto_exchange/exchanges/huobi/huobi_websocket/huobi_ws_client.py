import logging
import time
from pprint import pprint

from crypto_exchange.exchanges.huobi.huobi_websocket.huobi_ws import HuoBi

logger = logging.getLogger(__name__)


def huobi_k_line(symbol: str, period: str):
    """
    订阅 KLine 数据
    :param symbol btcusdt, ethusdt, ltcusdt, etcusdt, bchusdt, ethbtc, ltcbtc, etcbtc, bchbtc...
    :param period 1min, 5min, 15min, 30min, 60min, 1day, 1mon, 1week, 1year
    :return:
    """
    huobi = HuoBi()
    huobi.send_sub("""{"sub": "market.%s.kline.%s","id": "id1"}""" % (symbol, period))
    yield from huobi.recv()


def huobi_req_k_line(symbol: str, period: str):
    """
    请求 KLine 数据
    :param symbol btcusdt, ethusdt, ltcusdt, etcusdt, bchusdt, ethbtc, ltcbtc, etcbtc, bchbtc...
    :param period 1min, 5min, 15min, 30min, 60min, 1day, 1mon, 1week, 1year
    :return:
    """
    huobi = HuoBi()
    huobi.send_sub("""{"req": "market.%s.kline.%s","id": "id1"}""" % (symbol, period))
    yield from huobi.recv()


def huobi_depth(symbol: str, depth_type: str):
    """
    订阅 Market Depth 数据
    :param symbol: btcusdt, ethusdt, ltcusdt, etcusdt, bchusdt, ethbtc, ltcbtc, etcbtc, bchbtc...
    :param depth_type: step0, step1, step2, step3, step4, step5（合并深度0-5）；step0时，不合并深度
    :return:
    """
    huobi = HuoBi()
    huobi.send_sub("""{"sub": "market.%s.depth.%s","id": "id1"}""" % (symbol, depth_type))
    yield from huobi.recv()


def huobi_trade_detail(symbol: str):
    """
    订阅 Trade Detail 数据
    :param symbol:
    :return:
    """
    huobi = HuoBi()
    huobi.send_sub("""{"sub": "market.%s.trade.detail","id": "id1"}""" % symbol)
    yield from huobi.recv()


def huobi_detail(symbol: str):
    """
    请求 Market Detail 数据
    :param symbol:
    :return:
    """
    huobi = HuoBi()
    huobi.send_sub("""{"sub": "market.%s.detail","id": "id1"}""" % symbol)
    yield from huobi.recv()


# 订阅 KLine 数据
# data = huobi_k_line('ethbtc', '1min')

# 订阅 Market Depth 数据
# data = huobi_depth('ethbtc', 'step1')

# 订阅 Trade Detail 数据
# data = huobi_trade_detail('ethbtc')

# 请求 Market Detail 数据
# data = huobi_detail('ethbtc')


for i in data:
    pprint(i)
