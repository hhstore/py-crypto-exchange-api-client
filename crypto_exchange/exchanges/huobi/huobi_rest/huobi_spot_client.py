import logging
from datetime import datetime

from crypto_exchange.exchanges.huobi.huobi_rest.huobi_rest import HuobiAPI

logger = logging.getLogger(__name__)
PARAMS_ERROR = 'params_error'
API_KEY = 'b313ab7a-7af2e128-ba036ea6-4acf6'
SECRET_KEY = 'eb60c766-702767da-3aaafaee-32381'
K_LINE_PERIOD = ('1min', '5min', '15min', '30min', '60min', '1day', '1mon', '1week', '1year')
DEPTH_TYPE = ('step0', 'step1', 'step2', 'step3', 'step4', 'step5')
ORDER_TYPE = ('buy-market', 'sell-market', 'buy-limit', 'sell-limit',
              'buy-ioc', 'sell-ioc', 'buy-limit-marker', 'sell-limit-marker')
ORDER_STATES = ('canceled', 'filled', 'partial-canceled', 'partial-filled', 'submitted')


def huobi_history_k_line(symbol: str, period: str, size: int = 150):
    """
    获取K线数据
    :param symbol:
    :param period:
    :param size
    :return:
    """
    try:
        size = int(size)
    except Exception as e:
        logger.error(e)
        return PARAMS_ERROR
    if size > 200 or size < 0:
        return PARAMS_ERROR
    if period not in K_LINE_PERIOD:
        return PARAMS_ERROR
    huobi = HuobiAPI(API_KEY, SECRET_KEY)
    result = huobi.history_k_line(symbol, period, size=size)
    return result


def huobi_detail_merged(symbol: str):
    """
    获取聚合行情
    :param symbol:
    :return:
    """
    huobi = HuobiAPI(API_KEY, SECRET_KEY)
    result = huobi.detail_merged(symbol)
    return result


def huobi_tickers(symbol: str = None):
    """
    获取行情数据
    :param symbol:
    :return:
    """
    huobi = HuobiAPI(API_KEY, SECRET_KEY)
    result = huobi.tickers(symbol=symbol)
    return result


def huobi_depth(symbol: str, depth_type: str):
    """
    获取 Market Depth 数据
    :param symbol:
    :param depth_type:
    :return:
    """
    if depth_type not in DEPTH_TYPE:
        return PARAMS_ERROR
    huobi = HuobiAPI(API_KEY, SECRET_KEY)
    result = huobi.depth(symbol, depth_type)
    return result


def huobi_trade_detail(symbol: str):
    """
    获取 Trade Detail 数据
    :param symbol:
    :return:
    """
    huobi = HuobiAPI(API_KEY, SECRET_KEY)
    result = huobi.trade_detail(symbol)
    return result


def huobi_history_trade(symbol: str, size: int):
    """
    批量获取最近的交易记录
    :param symbol:
    :param size:
    :return:
    """
    try:
        size = int(size)
    except Exception as e:
        logger.error(e)
        return PARAMS_ERROR
    huobi = HuobiAPI(API_KEY, SECRET_KEY)
    result = huobi.history_trade(symbol, size)
    return result


def huobi_trade_24_detail(symbol: str):
    """
    获取 Market Detail 24小时成交量数据
    :param symbol:
    :return:
    """
    huobi = HuobiAPI(API_KEY, SECRET_KEY)
    result = huobi.trade_24_detail(symbol)
    return result


def huobi_symbols(site: str = None):
    """
    默认 查询Pro站支持的所有交易对及精度
    查询HADAX站支持的所有交易对及精度
    :param site:
    :return:
    """
    huobi = HuobiAPI(API_KEY, SECRET_KEY)
    result = huobi.symbols(site)
    return result


def huobi_currency(site: str = None):
    """
    默认 查询Pro站支持的所有币种
    查询HADAX站支持的所有币种
    :param site:
    :return:
    """
    huobi = HuobiAPI(API_KEY, SECRET_KEY)
    result = huobi.currency(site)
    return result


def huobi_timestamp():
    """
    查询系统当前时间
    :return:
    """
    huobi = HuobiAPI(API_KEY, SECRET_KEY)
    result = huobi.timestamp()
    return result


account_id = None


async def huobi_account(api_key: str, secret_key: str):
    """
    查询当前用户的所有账户(即account-id)，Pro站和HADAX account-id通用
    :param api_key
    :param secret_key
    :return:
    """
    global account_id
    huobi = HuobiAPI(api_key, secret_key)
    account_id = await huobi.account()

    return account_id


async def huobi_account_balance(api_key: str, secret_key: str, site: str = None):
    """
    默认 查询Pro站指定账户的余额
    查询HADAX站指定账户的余额
    :param api_key
    :param secret_key
    :param site:
    :return:
    """
    global account_id
    if not account_id:
        account_id = await huobi_account(api_key, secret_key)

        account_id = account_id[3]['data'][0]['id']
    try:
        int(account_id)
    except Exception as e:
        logger.error(e)
        return PARAMS_ERROR
    huobi = HuobiAPI(API_KEY, SECRET_KEY)
    result = huobi.account_balance(account_id, site)
    return result


async def huobi_spot_place_order(api_key: str, secret_key: str, symbol: str,
                                 order_type: str, amount: str, price: str = None,
                                 source: str = 'api',
                                 site: str = None):
    """
    默认 Pro站下单
    HADAX站下单
    :param api_key
    :param secret_key
    :param symbol:
    :param order_type:
    :param amount:
    :param price:
    :param source:
    :param site:
    :return:
    """
    global account_id
    if not account_id:
        account_id = await huobi_account(api_key, secret_key)

        account_id = account_id[3]['data'][0]['id']
    try:
        int(account_id)
    except Exception as e:
        logger.error(e)
        return PARAMS_ERROR
    if order_type not in ORDER_TYPE:
        return PARAMS_ERROR
    if order_type in ('buy-market', 'sell-market'):
        price = None

    huobi = HuobiAPI(api_key, secret_key)
    return await huobi.orders_place(account_id, amount, source, symbol, order_type, price, site)


async def huobi_open_orders(api_key: str, secret_key: str, symbol: str = None, side: str = None, size: int = 10):
    """
    获取所有当前帐号下未成交订单
    :param api_key:
    :param secret_key:
    :param symbol:
    :param side:
    :param size:
    :return:
    """
    global account_id
    if not account_id:
        account_id = await huobi_account(api_key, secret_key)

        account_id = account_id[3]['data'][0]['id']
    if symbol is None:
        account_id = None
    if account_id is None:
        symbol = None
    if side and side not in ('buy', 'sell'):
        return PARAMS_ERROR
    try:
        if size < 0 or size > 500:
            return PARAMS_ERROR
    except Exception as e:
        logger.error(e)
        return PARAMS_ERROR

    huobi = HuobiAPI(API_KEY, SECRET_KEY)
    result = huobi.open_orders(account_id, symbol, side, size)
    return result


async def huobi_spot_cancel_order(api_key: str, secret_key: str, order_id: str):
    """
    申请撤销一个订单请求
    :param api_key
    :param secret_key
    :param order_id:
    :param symbol
    :return:
    """
    try:
        int(order_id)
    except Exception as e:
        logger.error(e)
        return PARAMS_ERROR
    huobi = HuobiAPI(api_key, secret_key)
    return await huobi.cancel_order(order_id)


def huobi_batch_cancel_orders(order_id: list):
    """
    批量撤销订单
    :param order_id:
    :return:
    """
    try:
        if len(list(order_id)) > 50 or len(list(order_id)) < 0:
            return PARAMS_ERROR
    except Exception as e:
        logger.error(e)
        return PARAMS_ERROR

    huobi = HuobiAPI(API_KEY, SECRET_KEY)
    result = huobi.batch_cancel_orders(order_id)
    return result


def huobi_batch_cancel_open_orders(account_id: str, symbol: str, side: str = None, size: int = 10):
    """
    批量取消符合条件的订单
    :param account_id:
    :param symbol:
    :param side:
    :param size:
    :return:
    """
    try:
        int(account_id)
        size = int(size)
    except Exception as e:
        logger.error(e)
        return PARAMS_ERROR
    if size > 100 or size < 0:
        return PARAMS_ERROR
    if side not in ('buy', 'sell'):
        return PARAMS_ERROR

    huobi = HuobiAPI(API_KEY, SECRET_KEY)
    result = huobi.batch_cancel_open_orders(account_id, symbol, side, size)
    return result


def huobi_order_detail(order_id: str):
    """
    查询某个订单详情
    :param order_id:
    :return:
    """
    try:
        int(order_id)
    except Exception as e:
        logger.error(e)
        return PARAMS_ERROR
    huobi = HuobiAPI(API_KEY, SECRET_KEY)
    result = huobi.order_detail(order_id)
    return result


def huobi_order_match_results(order_id: str):
    """
    查询某个订单的成交明细
    :param order_id:
    :return:
    """
    try:
        int(order_id)
    except Exception as e:
        logger.error(e)
        return PARAMS_ERROR
    huobi = HuobiAPI(API_KEY, SECRET_KEY)
    result = huobi.order_match_results(order_id)
    return result


def huobi_orders_query(symbol: str, states: str, order_type: str = None, start_date: str = None,
                       end_date: str = None, id_from: str = None, direct: str = None, size: str = None):
    """
    查询当前委托、历史委托
    :param symbol:
    :param states:
    :param order_type:
    :param start_date:
    :param end_date:
    :param id_from:
    :param direct:
    :param size:
    :return:
    """
    try:
        datetime.strptime(start_date, '%Y-%m-%d')
        datetime.strptime(end_date, '%Y-%m-%d')
    except Exception as e:
        logger.error(e)
        return PARAMS_ERROR
    if order_type and order_type not in ORDER_TYPE:
        return PARAMS_ERROR
    if direct and direct not in ('prev', 'next'):
        return PARAMS_ERROR
    try:
        for i in states.split(','):
            if i not in ORDER_STATES:
                return PARAMS_ERROR
    except Exception as e:
        logger.error(e)
        return PARAMS_ERROR

    huobi = HuobiAPI(API_KEY, SECRET_KEY)
    result = huobi.orders_query(symbol, states, order_type, start_date, end_date, id_from, direct, size)
    return result


def huobi_order_query_match_results(symbol: str, order_type: str = None, start_date: str = None,
                                    end_date: str = None, id_from: str = None, direct: str = None, size: str = None):
    """
    查询当前成交、历史成交
    :param symbol:
    :param order_type:
    :param start_date:
    :param end_date:
    :param id_from:
    :param direct:
    :param size:
    :return:
    """
    try:
        datetime.strptime(start_date, '%Y-%m-%d')
        datetime.strptime(end_date, '%Y-%m-%d')
        int(id_from)
        int(size)
    except Exception as e:
        logger.error(e)
        return PARAMS_ERROR
    if order_type and order_type not in ORDER_TYPE:
        return PARAMS_ERROR
    if direct and direct not in ('prev', 'next'):
        return PARAMS_ERROR
    try:
        for i in order_type.split(','):
            if i not in ORDER_TYPE:
                return PARAMS_ERROR
    except Exception as e:
        logger.error(e)
        return PARAMS_ERROR

    huobi = HuobiAPI(API_KEY, SECRET_KEY)
    result = huobi.order_query_match_results(symbol, order_type, start_date, end_date, id_from, direct, size)
    return result


def huobi_withdraw(address: str, amount: str, currency: str, fee: str = None, addr_tag=None):
    """
    申请提现虚拟币
    :param address:
    :param amount:
    :param currency:
    :param fee:
    :param addr_tag:
    :return:
    """
    huobi = HuobiAPI(API_KEY, SECRET_KEY)
    result = huobi.withdraw(address, amount, currency, fee, addr_tag)
    return result


def huobi_withdraw_cancel(withdraw_id: int):
    """
    申请取消提现虚拟币
    :return:
    """
    huobi = HuobiAPI(API_KEY, SECRET_KEY)
    result = huobi.withdraw_cancel(withdraw_id)
    return result


def huobi_query_deposit_withdraw(currency: str, query_type: str, id_from: str = None, size: str = None):
    """
    查询虚拟币充提记录
    :param currency:
    :param query_type:
    :param id_from:
    :param size:
    :return:
    """
    huobi = HuobiAPI(API_KEY, SECRET_KEY)
    result = huobi.query_deposit_withdraw(currency, query_type, id_from, size)
    return result
