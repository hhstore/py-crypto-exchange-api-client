import logging

from crypto_exchange.exchanges.huobi.huobi_rest.huobi_rest import HuobiAPI

logger = logging.getLogger(__name__)
PARAMS_ERROR = 'params_error'
API_KEY = 'b313ab7a-7af2e128-ba036ea6-4acf6'
SECRET_KEY = 'eb60c766-702767da-3aaafaee-32381'
K_LINE_PERIOD = ('1min', '5min', '15min', '30min', '60min', '1day', '1mon', '1week', '1year')


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


def huobi_account():
    """
    查询当前用户的所有账户(即account-id)，Pro站和HADAX account-id通用
    :return:
    """
    huobi = HuobiAPI(API_KEY, SECRET_KEY)
    result = huobi.account()
    return result
