import logging

from crypto_exchange.exchanges.okex.okex_rest.okex_spot import OKExSpot
from crypto_exchange.conf.exchange import Config

logger = logging.getLogger(__name__)

API_KEY = Config.exchange_api_key['okex']['public_key']
SECRET_KEY = Config.exchange_api_key['okex']['secret_key']


def okex_spot_ticker(symbol: str):
    """
    获取币币交易行情
    :param symbol: 交易对
    :return: is_ok, status_code, response, result
    """
    # 校验参数
    okex_spot = OKExSpot(api_key=API_KEY, secret_key=SECRET_KEY)
    result = okex_spot.ticker(symbol)
    return result


def okex_spot_depth(symbol: str, size=200):
    """
    获取币币市场深度
    :param symbol: 交易对
    :param size: value:1-200
    :return: is_ok, status_code, response, result
    """
    # 校验参数
    if size < 1 or size > 200:
        return '参数错误'
    okex_spot = OKExSpot(api_key=API_KEY, secret_key=SECRET_KEY)
    result = okex_spot.depth(symbol, size=size)
    return result


def okex_spot_tradesinfo(symbol: str, since=None):
    """
    获取币币交易信息，60条
    :param symbol: 交易对
    :return:is_ok, status_code, response, result
    """
    if since < 0:
        return '参数错误'

    okex_spot = OKExSpot(api_key=API_KEY, secret_key=SECRET_KEY)
    result = okex_spot.tradesinfo(symbol)
    return result


def okex_spot_kline(symbol, type, size=None, since=None):
    """
    获取币币K线数据，每个周期数据条数2000左右
    param symbol: 交易对
    :param type: 1min/3min/5min/15min/30min/1day/3day/1week/1hour/2hour/4hour/6hour/12hour
    :param size: 获取数据的条数，默认全部获取
    :param since: 时间戳，返回时间戳以后的数据，默认全部获取
    :return: is_ok, status_code, response, result
    """
    # 校验参数
    if type not in (
        '1min', '3min', '5min', '15min', '30min', '1day', '3day', '1week', '1hour', '2hour', '4hour', '6hour',
        '12hour'):
        return '参数错误'

    okex_spot = OKExSpot(api_key=API_KEY, secret_key=SECRET_KEY)
    result = okex_spot.kine(symbol, type, size, since)
    return result


def okex_spot_userinfo():
    """
    获取用户信息,访问频率6次/2秒
    :return:is_ok, status_code, response, result
    """
    okex_spot = OKExSpot(api_key=API_KEY, secret_key=SECRET_KEY)
    result = okex_spot.userinfo()
    return result


def okex_spot_trade(symbol: str, type: str, price: float, amount: float):
    """
    下单交易，访问频率20次/2秒
    市价买单不传amount，市价买单需传peice作为买入总金额
    市价卖单不传price，
    卖单 amount一位小数
    卖单
    :param symbol: 交易对
    :param type: 买卖类型
    :param price: 下单价格，
    :param amount: 交易数量，
    :return: is_ok, status_code, response, result
    """
    # 校验参数
    if type not in ('buy', 'sell', 'buy_market', 'sell_market'):
        return '参数错误'
    try:
        price = float(price)
        amount = round(float(amount), 1)
    except Exception as e:
        return '参数错误'
    if type == 'sell_market':
        price = None
    if type == 'buy_market':
        amount = None

    okex_spot = OKExSpot(api_key=API_KEY, secret_key=SECRET_KEY)
    result = okex_spot.trade(symbol, type, price, amount)
    return result


def okex_spot_batch_trade(symbol: str, orders_data: str, type=None):
    """
    批量下单，访问频率20次/2秒 最大下单量为5
    :param symbol:交易对
    :param type: buy/sell/
    :param order_data: '[{价格,数量，买卖类型},{}]'
    :return: is_ok, status_code, response, result
    """
    # 校验参数
    if type not in ('buy', 'sell'):
        return '参数错误'
    try:
        if len(eval(orders_data)) > 5 or len(eval(orders_data)) < 1:
            return '参数错误'
    except Exception as e:
        pass

    okex_spot = OKExSpot(api_key=API_KEY, secret_key=SECRET_KEY)
    result = okex_spot.batch_trade(symbol, orders_data, type=None)
    return result


def okex_spot_cancel_order(symbol: str, order_id: str):
    """
    撤销订单 访问频率20次/2秒 一次最多三个
    :param symbol: 交易对
    :param order_id: 订单ID，多个订单已','分隔
    :return: is_ok, status_code, response, result
    """
    # 校验参数
    try:
        if len(eval(order_id)) > 3 or len(eval(order_id)) < 1:
            return '参数错误'
    except Exception as e:
        pass
    okex_spot = OKExSpot(api_key=API_KEY, secret_key=SECRET_KEY)
    result = okex_spot.cancel_order(symbol, order_id)
    return result


def okex_spot_order_info(symbol: str, order_id: int):
    """
    获取用户的订单信息 访问频率 20次/2秒(未成交)
    :param symbol:
    :param order_id: -1:未完成订单，否则查询相应订单号的订单
    :return:
    """

    okex_spot = OKExSpot(api_key=API_KEY, secret_key=SECRET_KEY)
    result = okex_spot.order_info(symbol, order_id)
    return result


def okex_spot_orders_info(symbol: str, order_id: str, type: int):
    """
    批量获取用户订单 访问频率20次/2次 最多50个订单
    :param symbol:
    :param order_id:多个订单ID中间以","分隔,一次最多允许查询50个订单
    :param type:查询类型 0:未完成的订单 1:已经完成的订单
    :return:
    """
    # 校验参数
    if type not in (0, 1):
        return '参数错误'
    try:
        if len(eval(order_id)) > 50 or len(eval(order_id)) < 1:
            return '参数错误'
    except Exception as e:
        pass

    okex_spot = OKExSpot(api_key=API_KEY, secret_key=SECRET_KEY)
    result = okex_spot.orders_info(symbol, order_id, type)
    return result


def okex_spot_order_history(symbol: str, status: int, current_page: int, page_length: int):
    """
    获取历史订单信息 只返回最近两天的信息
    :param symbol:
    :param status:查询状态 0：未完成的订单 1：已经完成的订单(最近两天的数据)
    :param current_page:当前页数
    :param page_length:每页数据条数，最多不超过200
    :return:
    """
    # 校验参数
    if status not in (0, 1):
        return '参数错误'
    if page_length > 200 or page_length < 0:
        return '参数错误'

    okex_spot = OKExSpot(api_key=API_KEY, secret_key=SECRET_KEY)
    result = okex_spot.order_history(symbol, status, current_page, page_length)
    return result


def okex_spot_order_wallet_info():
    """
    获取用户钱包账户信息
    :return:
    """
    okex_spot = OKExSpot(api_key=API_KEY, secret_key=SECRET_KEY)
    result = okex_spot.wallet_info()
    return result
