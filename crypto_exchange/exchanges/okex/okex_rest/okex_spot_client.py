import logging

from crypto_exchange.conf.exchange import Config
from crypto_exchange.exchanges.okex.okex_rest.okex_spot import OKExSpot

logger = logging.getLogger(__name__)

API_KEY = Config.exchange_api_key['okex']['public_key']
SECRET_KEY = Config.exchange_api_key['okex']['secret_key']
PARAMS_ERROR = 'params_error'
K_LINE_TYPE = (
    '1min', '3min', '5min', '15min', '30min', '1day', '3day', '1week', '1hour', '2hour', '4hour', '6hour',
    '12hour')
TRADE_TYPE = ('buy', 'sell', 'buy_market', 'sell_market')  # 限价单(buy/sell) 市价单(buy_market/sell_market)
BATCH_TRADE_TYPE = ('buy', 'sell')  # 限价单(buy/sell)
ORDERS_INFO_TYPE = (0, 1)  # 0:未完成的订单 1:已经完成的订单
ORDER_HISTORY_STATUS = (0, 1)  # 0：未完成的订单 1：已经完成的订单(最近两天的数据)
ACCOUNT_RECORDS_TYPE = (0, 1)  # 0：充值 1 ：提现
FUNDS_TRANSFER_TYPE = (1, 3, 6)  # 1：币币账户 3：合约账户 6：我的钱包


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


def okex_spot_depth(symbol: str, size: int = 200):
    """
    获取币币市场深度
    :param symbol: 交易对
    :param size: value:1-200
    :return: is_ok, status_code, response, result
    """
    # 校验参数
    try:
        if 1 <= size <= 200:
            size = size
        else:
            return PARAMS_ERROR
    except Exception as e:
        logger.error(e)
        return PARAMS_ERROR
    okex_spot = OKExSpot(api_key=API_KEY, secret_key=SECRET_KEY)
    result = okex_spot.depth(symbol, size=size)
    return result


def okex_spot_trades_info(symbol: str, since: int = None):
    """
    获取币币交易信息，60条
    :param symbol: 交易对
    :param since: tid:交易记录ID(返回数据不包括当前tid值,最多返回60条数据)
    :return:is_ok, status_code, response, result
    """
    if since:
        try:
            since = int(since)
            if since < 0:
                return PARAMS_ERROR
        except Exception as e:
            logger.error(e)
            return PARAMS_ERROR
    okex_spot = OKExSpot(api_key=API_KEY, secret_key=SECRET_KEY)
    result = okex_spot.trades_info(symbol, since)
    return result


def okex_spot_k_line(symbol: str, k_line_type: str, size: int = None, since: int = None):
    """
    获取币币K线数据，每个周期数据条数2000左右
    :param symbol: 交易对
    :param k_line_type: 1min/3min/5min/15min/30min/1day/3day/1week/1hour/2hour/4hour/6hour/12hour
    :param size: 获取数据的条数，默认全部获取
    :param since: 时间戳，返回时间戳以后的数据，默认全部获取
    :return: is_ok, status_code, response, result
    """
    # 校验参数
    if k_line_type not in K_LINE_TYPE:
        return PARAMS_ERROR
    try:
        size = int(size)
        since = int(since)
    except Exception as e:
        logger.error(e)
        return PARAMS_ERROR
    okex_spot = OKExSpot(api_key=API_KEY, secret_key=SECRET_KEY)
    result = okex_spot.k_line(symbol, k_line_type, size, since)
    return result


def okex_spot_user_info():
    """
    获取用户信息,访问频率6次/2秒
    :return:is_ok, status_code, response, result
    """
    okex_spot = OKExSpot(api_key=API_KEY, secret_key=SECRET_KEY)
    result = okex_spot.user_info()
    return result


def okex_spot_trade(symbol: str, trade_type: str, price: float, amount: float):
    """
    下单交易，访问频率20次/2秒
    市价买单不传amount，市价买单需传peice作为买入总金额
    市价卖单不传price，
    卖单 amount一位小数
    卖单
    :param symbol: 交易对
    :param trade_type: 买卖类型
    :param price: 下单价格，
    :param amount: 交易数量，
    :return: is_ok, status_code, response, result
    """
    # 校验参数
    if trade_type not in TRADE_TYPE:
        return PARAMS_ERROR
    try:
        price = float(price)
        amount = round(float(amount), 1)
    except Exception as e:
        logger.error(e)
        return PARAMS_ERROR
    if trade_type == 'sell_market':
        price = None
    if trade_type == 'buy_market':
        amount = None

    okex_spot = OKExSpot(api_key=API_KEY, secret_key=SECRET_KEY)
    result = okex_spot.trade(symbol, trade_type, price, amount)
    return result


def okex_spot_batch_trade(symbol: str, orders_data: str, trade_type=None):
    """
    批量下单，访问频率20次/2秒 最大下单量为5
    :param symbol:交易对
    :param trade_type: buy/sell/
    :param orders_data: '[{价格,数量，买卖类型},{}]'
    :return: is_ok, status_code, response, result
    """
    # 校验参数
    if trade_type not in BATCH_TRADE_TYPE:
        return PARAMS_ERROR
    try:
        if len(eval(orders_data)) > 5 or len(eval(orders_data)) < 1:
            return PARAMS_ERROR
    except Exception as e:
        logger.error(e)
        return PARAMS_ERROR

    okex_spot = OKExSpot(api_key=API_KEY, secret_key=SECRET_KEY)
    result = okex_spot.batch_trade(symbol, orders_data, trade_type=trade_type)
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
            return PARAMS_ERROR
    except Exception as e:
        logger.error(e)
        return PARAMS_ERROR

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
    try:
        order_id = int(order_id)
    except Exception as e:
        logger.error(e)
        return PARAMS_ERROR
    okex_spot = OKExSpot(api_key=API_KEY, secret_key=SECRET_KEY)
    result = okex_spot.order_info(symbol, order_id)
    return result


def okex_spot_orders_info(symbol: str, order_id: str, info_type: int):
    """
    批量获取用户订单 访问频率20次/2次 最多50个订单
    :param symbol:
    :param order_id:多个订单ID中间以","分隔,一次最多允许查询50个订单
    :param info_type:查询类型 0:未完成的订单 1:已经完成的订单
    :return:
    """
    # 校验参数
    if info_type not in ORDERS_INFO_TYPE:
        return PARAMS_ERROR
    try:
        if len(eval(order_id)) > 50 or len(eval(order_id)) < 1:
            return PARAMS_ERROR
    except Exception as e:
        logger.error(e)
        return PARAMS_ERROR

    okex_spot = OKExSpot(api_key=API_KEY, secret_key=SECRET_KEY)
    result = okex_spot.orders_info(symbol, order_id, info_type)
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
    try:
        status = int(status)
        current_page = int(current_page)
        page_length = int(page_length)
    except Exception as e:
        logger.error(e)
        return PARAMS_ERROR
    if status not in ORDER_HISTORY_STATUS:
        return PARAMS_ERROR
    if page_length > 200 or page_length < 0:
        return PARAMS_ERROR

    okex_spot = OKExSpot(api_key=API_KEY, secret_key=SECRET_KEY)
    result = okex_spot.order_history(symbol, status, current_page, page_length)
    return result


def okex_withdraw(symbol: str, charge_fee: float, trade_pwd: str, withdraw_address: str, withdraw_amount: float,
                  target: str = 'OKEX'):
    """
    提币
    :param symbol: 交易对
    :param charge_fee: 网路手续费 BTC[0.002，0.005] LTC[0.001，0.2] ETH[0.01] ETC[0.0001，0.2] BCH范围 [0.0005，0.002]
    :param trade_pwd: 交易密码
    :param withdraw_address: 提币认证地址
    :param withdraw_amount: 提币数量
    :param target: 地址类型
    :return:
    """
    try:
        charge_fee = float(charge_fee)
        withdraw_amount = float(withdraw_amount)
    except Exception as e:
        logger.error(e)
        return PARAMS_ERROR

    okex_spot = OKExSpot(api_key=API_KEY, secret_key=SECRET_KEY)
    result = okex_spot.withdraw(symbol, charge_fee, trade_pwd, withdraw_address, withdraw_amount, target)
    return result


def okex_withdraw_info(symbol: str, withdraw_id: str):
    """
    查询提币BTC/LTC/ETH/ETC/BCH信息
    :param symbol:
    :param withdraw_id:
    :return:
    """
    okex_spot = OKExSpot(api_key=API_KEY, secret_key=SECRET_KEY)
    result = okex_spot.withdraw_info(symbol, withdraw_id)
    return result


def okex_account_records(symbol: str, account_type: int, current_page: int, page_length: int):
    """
    获取用户提现/充值记录
    :param symbol:
    :param account_type:
    :param current_page:
    :param page_length:
    :return:
    """
    try:
        account_type = int(account_type)
        current_page = int(current_page)
        page_length = int(page_length)
    except Exception as e:
        logger.error(e)
        return PARAMS_ERROR

    if account_type not in ACCOUNT_RECORDS_TYPE:
        return PARAMS_ERROR
    if page_length < 0 or page_length > 50:
        return PARAMS_ERROR

    okex_spot = OKExSpot(api_key=API_KEY, secret_key=SECRET_KEY)
    result = okex_spot.account_records(symbol, account_type, current_page, page_length)
    return result


def okex_funds_transfer(symbol: str, amount: int, funds_from: int, funds_to: int):
    """
    资金划转
    :param symbol:
    :param amount:
    :param funds_from:
    :param funds_to:
    :return:
    """
    try:
        amount = int(amount)
        funds_from = int(funds_from)
        funds_to = int(funds_to)
    except Exception as e:
        logger.error(e)
        return PARAMS_ERROR
    if funds_to not in FUNDS_TRANSFER_TYPE:
        return PARAMS_ERROR
    if funds_from not in FUNDS_TRANSFER_TYPE:
        return PARAMS_ERROR

    okex_spot = OKExSpot(api_key=API_KEY, secret_key=SECRET_KEY)
    result = okex_spot.account_records(symbol, amount, funds_from, funds_to)
    return result


def okex_wallet_info():
    """
    获取用户钱包账户信息
    :return:
    """
    okex_spot = OKExSpot(api_key=API_KEY, secret_key=SECRET_KEY)
    result = okex_spot.wallet_info()
    return result
