import logging

from pprint import pprint

from crypto_exchange.exchanges.okex.okex_websocket.okex_ws import OKEx

logger = logging.getLogger(__name__)
API_KEY = "3b773537-bbae-4db9-9a9b-42069d7e1fbb"
SECRET_KEY = "EFAABB4F616059E45557329A86D2B77C"
URL = "wss://real.okex.com:10440/websocket/okexapi"


def okex_futures_ticker(symbol: str, cycle: str):
    """
    订阅合约行情
    :param symbol 值为：btc, ltc, eth, etc, bch,eos,xrp,btg
    :param cycle 值为：this_week, next_week, quarter
    :return:
    """
    okex_spot = OKEx(url=URL)
    okex_spot.send_sub("{'event':'addChannel','channel':'ok_sub_futureusd_%s_ticker_%s'}" % (symbol, cycle))

    yield from okex_spot.recv()


def okex_futures_k_line(symbol: str, cycle: str, time: str):
    """
    订阅合约K线数据
    :param symbol: 值为：btc, ltc, eth, etc, bch,eos,xrp,btg
    :param cycle: 值为：this_week, next_week, quarter
    :param time: 值为：1min, 3min, 5min, 15min, 30min, 1hour, 2hour, 4hour, 6hour, 12hour, day, 3day, week
    :return:
    """
    okex_spot = OKEx(url=URL)
    okex_spot.send_sub("{'event':'addChannel','channel':'ok_sub_futureusd_%s_kline_%s_%s'}" % (symbol, cycle, time))

    yield from okex_spot.recv()


def okex_futures_depth(symbol: str, cycle: str):
    """
    订阅合约市场深度(200增量数据返回)
    :param symbol 值为：btc, ltc, eth, etc, bch,eos,xrp,btg
    :param cycle 值为：this_week, next_week, quarter
    :return:
    """
    okex_spot = OKEx(url=URL)
    okex_spot.send_sub("{'event':'addChannel','channel':'ok_sub_futureusd_%s_depth_%s'}" % (symbol, cycle))

    yield from okex_spot.recv()


def okex_futures_depth_size(symbol: str, cycle: str, size: str):
    """
    订阅合约市场深度(全量返回)
    :param symbol: 值为：btc, ltc, eth, etc, bch,eos,xrp,btg
    :param cycle: 值为：this_week, next_week, quarter
    :param size: 值为：5, 10, 20(获取深度条数)
    :return:
    """
    okex_spot = OKEx(url=URL)
    okex_spot.send_sub("{'event':'addChannel','channel':'ok_sub_futureusd_%s_depth_%s_%s'}" % (symbol, cycle, size))

    yield from okex_spot.recv()


def okex_futures_trade(symbol: str, cycle: str):
    """
    订阅合约交易信息
    :param symbol 值为：btc, ltc, eth, etc, bch,eos,xrp,btg
    :param cycle 值为：this_week, next_week, quarter
    :return:
    """
    okex_spot = OKEx(url=URL)
    okex_spot.send_sub("{'event':'addChannel','channel':'ok_sub_futureusd_%s_trade_%s'}" % (symbol, cycle))

    yield from okex_spot.recv()


def okex_futures_index(symbol: str):
    """
    订阅合约指数
    :param symbol 值为：btc, ltc, eth, etc, bch,eos,xrp,btg
    :return:
    """
    okex_spot = OKEx(url=URL)
    okex_spot.send_sub("{'event':'addChannel','channel':'ok_sub_futureusd_%s_index'}" % symbol)

    yield from okex_spot.recv()


def okex_futures_forecast_price(symbol: str):
    """
    合约预估交割价格
    # TODO 无需订阅，交割前一小时自动返回
    :param symbol 值为：btc, ltc, eth, etc, bch,eos,xrp,btg
    :return:
    """
    okex_spot = OKEx(url=URL)
    okex_spot.send_sub("{'event':'addChannel','channel':'ok_sub_futureusd_%s_forecast_price'}" % symbol)

    yield from okex_spot.recv()


# 订阅合约行情
# data = okex_futures_ticker('btc', 'this_week')

# 订阅合约K线数据
# data = okex_futures_k_line('btc', 'this_week', '1min')

# 订阅合约市场深度(200增量数据返回)
# data = okex_futures_depth('btc', 'this_week')

# 订阅合约市场深度(全量返回)
# data = okex_futures_depth_size('btc','this_week','20')

# 订阅合约交易信息
# data = okex_futures_trade('btc', 'this_week')

# 订阅合约指数
# data = okex_futures_index('btc')

# 合约预估交割价格
# data = okex_futures_forecast_price('btc')

for i in data:
    pprint(i)
