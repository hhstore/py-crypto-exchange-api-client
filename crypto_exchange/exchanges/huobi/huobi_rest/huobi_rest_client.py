import logging

from crypto_exchange.exchanges.huobi.huobi_rest.huobi_rest import HuobiAPI

logger = logging.getLogger(__name__)
PARAMS_ERROR = 'params_error'
API_KEY = 'b313ab7a-7af2e128-ba036ea6-4acf6'
SECRET_KEY = 'eb60c766-702767da-3aaafaee-32381'
K_LINE_PERIOD = ('1min', '5min', '15min', '30min', '60min', '1day', '1mon', '1week', '1year')
DEPTH_TYPE = ('step0', 'step1', 'step2', 'step3', 'step4', 'step5')


def huobi_history_k_line(symbol: str, period: str, size: int = 150):
    """
    获取K线数据
    :param symbol:
    :param period:
    :param size
    :return:
    """
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


def huobi_account():
    """
    查询当前用户的所有账户(即account-id)，Pro站和HADAX account-id通用
    :return:
    """
    huobi = HuobiAPI(API_KEY, SECRET_KEY)
    result = huobi.account()
    return result
