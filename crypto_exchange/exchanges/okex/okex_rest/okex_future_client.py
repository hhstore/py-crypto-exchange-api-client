import logging
import re
from datetime import datetime

from crypto_exchange.conf.exchange import Config
from crypto_exchange.exchanges.okex.okex_rest.okex_future import OKExFuture

logger = logging.getLogger(__name__)

API_KEY = Config.exchange_api_key['okex']['public_key']
SECRET_KEY = Config.exchange_api_key['okex']['secret_key']
K_LINE_TYPE = (
    '1min', '3min', '5min', '15min', '30min', '1day', '3day', '1week', '1hour', '2hour', '4hour', '6hour',
    '12hour')
CONTRACT_TYPE = ('this_week', 'next_week', 'quarter')  # this_week:当周 next_week:下周 quarter:季度
FUTURE_TRADE_TYPE = ('1', '2', '3', '4')  # 1:开多 2:开空 3:平多 4:平空
PARAMS_ERROR = 'params_error'


async def okex_future_ticker(symbol: str, contract_type: str):
    """
    获取合约行情数据
    :param symbol: 交易对
    :param contract_type: 合约类型
    :return: is_ok, status_code, response, result
    """
    # 校验参数
    if contract_type not in CONTRACT_TYPE:
        return PARAMS_ERROR

    okex_future = OKExFuture(api_key=API_KEY, secret_key=SECRET_KEY)

    return await okex_future.future_ticker(symbol, contract_type)


async def okex_future_depth(symbol: str, contract_type: str, size: int = 200, merge: int = 0):
    """
    获取合约深度信息
    :param symbol: 交易对
    :param contract_type: 合约类型
    :param size: value
    :param merge: 合并深度
    :return:
    """
    # 校验参数
    if contract_type not in CONTRACT_TYPE:
        return PARAMS_ERROR
    try:
        size = int(size)
        merge = int(merge)
    except Exception as e:
        logger.error(e)
        return PARAMS_ERROR
    if merge not in (0, 1):
        return PARAMS_ERROR
    if size < 1 or size > 200:
        return PARAMS_ERROR

    okex_future = OKExFuture(api_key=API_KEY, secret_key=SECRET_KEY)
    return await okex_future.future_depth(symbol, contract_type, size, merge)


async def okex_future_trades(symbol: str, contract_type: str):
    """
    获取合约交易记录信息
    :param symbol:
    :param contract_type:
    :return:
    """
    if contract_type not in CONTRACT_TYPE:
        return PARAMS_ERROR

    okex_future = OKExFuture(api_key=API_KEY, secret_key=SECRET_KEY)
    return await okex_future.future_trades(symbol, contract_type)


async def okex_future_index(symbol: str):
    """
    获取合约指数信息
    :param symbol:
    :return:
    """
    okex_future = OKExFuture(api_key=API_KEY, secret_key=SECRET_KEY)
    return await okex_future.future_index(symbol)


async def okex_future_estimated_price(symbol: str):
    """
    获取交割预估价
    :param symbol:
    :return:
    """
    okex_future = OKExFuture(api_key=API_KEY, secret_key=SECRET_KEY)
    return await okex_future.future_estimated_price(symbol)


async def okex_future_k_line(symbol: str, k_line_type: str, contract_type: str, size: int = 0, since: int = 0):
    """
    获取合约K线信息
    :param symbol:
    :param k_line_type:
    :param contract_type:
    :param size:
    :param since:
    :return:
    """
    try:
        size = int(size)
        since = int(since)
    except Exception as e:
        logger.error(e)
        return PARAMS_ERROR
    if k_line_type not in K_LINE_TYPE:
        return PARAMS_ERROR
    if contract_type not in CONTRACT_TYPE:
        return PARAMS_ERROR

    okex_future = OKExFuture(api_key=API_KEY, secret_key=SECRET_KEY)
    return await okex_future.future_k_line(symbol, k_line_type, contract_type, size, since)


async def okex_future_hold_amount(symbol: str, contract_type: str):
    """
    获取当前可用合约总持仓量
    :param symbol:
    :param contract_type:
    :return:
    """
    if contract_type not in CONTRACT_TYPE:
        return PARAMS_ERROR

    okex_future = OKExFuture(api_key=API_KEY, secret_key=SECRET_KEY)
    return await okex_future.future_hold_amount(symbol, contract_type)


async def okex_future_price_limit(symbol: str, contract_type: str):
    """
    获取合约最高限价和最低限价
    :param symbol:
    :param contract_type:
    :return:
    """
    if contract_type not in CONTRACT_TYPE:
        return PARAMS_ERROR

    okex_future = OKExFuture(api_key=API_KEY, secret_key=SECRET_KEY)
    return await okex_future.future_price_limit(symbol, contract_type)


async def okex_future_user_info():
    """
    获取合约账户信息(全仓) 访问频率 10次/2秒
    :return:
    """
    # TODO 校验是否为全仓

    okex_future = OKExFuture(api_key=API_KEY, secret_key=SECRET_KEY)
    return await okex_future.future_user_info()


async def okex_future_user_info_4fix():
    """
    获取逐仓合约账户信息
    :return:
    """
    # TODO 校验是否为逐仓

    okex_future = OKExFuture(api_key=API_KEY, secret_key=SECRET_KEY)
    return await okex_future.future_user_info_4fix()


async def okex_future_position(symbol: str, contract_type: str):
    """
    获取合约全仓持仓信息 访问频率 10次/2秒
    :param symbol: 交易对
    :param contract_type: 合约类型: this_week:当周 next_week:下周 quarter:季度
    :return:
    """
    # TODO 校验是否为全仓
    if contract_type not in CONTRACT_TYPE:
        return PARAMS_ERROR

    okex_future = OKExFuture(api_key=API_KEY, secret_key=SECRET_KEY)

    return await okex_future.future_position(symbol, contract_type)


async def okex_future_position_4fix(symbol: str, contract_type: str, data_type=None):
    """
    逐仓用户持仓查询 访问频率 10次/2秒
    :param symbol:交易对
    :param contract_type:合约类型: this_week:当周 next_week:下周 quarter:季度
    :param data_type:默认返回10倍杠杆持仓 type=1 返回全部持仓数据
    :return:
    """
    # TODO 校验是否为逐仓
    if contract_type not in CONTRACT_TYPE:
        return PARAMS_ERROR

    okex_future = OKExFuture(api_key=API_KEY, secret_key=SECRET_KEY)
    return await okex_future.future_position_4fix(symbol, contract_type, data_type=data_type)


async def okex_future_place_order(api_key:str,secret_key:str,symbol: str, contract_type: str, price: str, amount: str, trade_type: str, match_price: str,
                            lever_rate: str):
    """
    合约下单 访问频率 5次/1秒(按币种单独计算)
    :param symbol:交易对
    :param contract_type:合约类型
    :param price:价格
    :param amount:委托数量
    :param trade_type:1:开多 2:开空 3:平多 4:平空
    :param match_price:是否为对手价 0:不是 1:是 ,当取值为1时,price无效
    :param lever_rate:TODO 杠杆倍数
    :return:
    """
    # 校验参数
    if contract_type not in CONTRACT_TYPE:
        return PARAMS_ERROR
    if trade_type not in FUTURE_TRADE_TYPE:
        return PARAMS_ERROR
    if match_price not in ('0', '1'):
        return PARAMS_ERROR

    okex_future = OKExFuture(api_key, secret_key)

    return await okex_future.future_trade(symbol, contract_type, price, amount, trade_type, match_price, lever_rate)


async def okex_future_batch_trade(symbol: str, contract_type: str, orders_data: str, lever_rate: str):
    """
    合约批量下单 访问频率 3次/1秒 最多一次下1-5个订单（按币种单独计算）
    :param symbol: 交易对
    :param contract_type:合约类型: this_week:当周 next_week:下周 quarter:季度
    :param orders_data:JSON类型的字符串 例：[{price:5,amount:2,type:1,match_price:1},{price:2,amount:3,type:1,match_price:1}] 最大下单量为5，
    :param lever_rate:杠杆倍数
    :return:
    """
    # 校验参数
    if contract_type not in CONTRACT_TYPE:
        return PARAMS_ERROR
    try:
        if len(re.findall('price', orders_data)) > 5 or len(re.findall('price', orders_data)) < 1:
            return PARAMS_ERROR
    except Exception as e:
        logger.error(e)
        return PARAMS_ERROR

    okex_future = OKExFuture(api_key=API_KEY, secret_key=SECRET_KEY)

    return await okex_future.future_batch_trade(symbol, contract_type, orders_data, lever_rate)


async def okex_future_cancel(symbol: str, contract_type: str, order_id: str):
    """
    取消合约订单 访问频率 2次/1秒，最多一次撤1-5个订单（按币种单独计算）
    :param symbol: 交易对
    :param contract_type: 合约类型: this_week:当周 next_week:下周 quarter:季度
    :param order_id: 订单ID(多个订单ID中间以","分隔,一次最多允许撤消5个订单)
    :return:
    """
    # 校验参数
    if contract_type not in CONTRACT_TYPE:
        return PARAMS_ERROR
    try:
        if len(re.findall(',', order_id)) > 5:
            return PARAMS_ERROR
    except Exception as e:
        logger.error(e)
        return PARAMS_ERROR

    okex_future = OKExFuture(api_key=API_KEY, secret_key=SECRET_KEY)

    return await okex_future.future_cancel(symbol, contract_type, order_id)


async def okex_future_trades_history(symbol: str, date: str, since: int):
    """
    获取合约交易历史(非个人) 访问频率 2次/2秒
    :param symbol: 交易对
    :param date: 合约交割时间，格式yyyy-MM-dd
    :param since:交易Id起始位置
    :return:
    """
    # 校验参数
    try:
        since = int(since)
        year_date, mon_date, day_date = date.split('-')
        datetime(int(year_date), int(mon_date), int(day_date))
    except Exception as e:
        logger.error(e)
        return PARAMS_ERROR

    okex_future = OKExFuture(api_key=API_KEY, secret_key=SECRET_KEY)

    return await okex_future.future_trades_history(symbol, date, since)


async def okex_future_order_info(symbol: str, contract_type: str, order_id: str, status: str, current_page: str,
                                 page_length: str):
    """
    获取合约订单信息
    :param symbol: 交易对
    :param contract_type:合约类型: this_week:当周 next_week:下周 quarter:季度
    :param order_id:订单ID -1:查询指定状态的订单，否则查询相应订单号的订单
    :param status:查询状态 1:未完成的订单 2:已经完成的订单
    :param current_page:当前页数
    :param page_length:每页获取条数，最多不超过50
    :return:
    """
    # 校验参数
    if contract_type not in CONTRACT_TYPE:
        return PARAMS_ERROR
    if status not in ('1', '2'):
        return PARAMS_ERROR
    try:
        int(current_page)
        int(order_id)
        if int(page_length) > 50:
            return PARAMS_ERROR
    except Exception as e:
        logger.error(e)
        return PARAMS_ERROR

    okex_future = OKExFuture(api_key=API_KEY, secret_key=SECRET_KEY)

    return await okex_future.future_order_info(symbol, contract_type, order_id, status, current_page, page_length)


async def okex_future_orders_info(symbol: str, contract_type: str, orders_id: str):
    """
    批量获取合约订单信息
    :param symbol: 交易对
    :param contract_type:合约类型: this_week:当周 next_week:下周 quarter:季度
    :param orders_id:订单ID(多个订单ID中间以","分隔,一次最多允许查询50个订单)
    :return:
    """
    # 校验参数
    if contract_type not in CONTRACT_TYPE:
        return PARAMS_ERROR
    try:
        if len(re.findall(',', orders_id)) >= 50:
            return PARAMS_ERROR
    except Exception as e:
        logger.error(e)
        return PARAMS_ERROR

    okex_future = OKExFuture(api_key=API_KEY, secret_key=SECRET_KEY)

    return await okex_future.future_orders_info(symbol, contract_type, orders_id)


async def okex_future_explosive(symbol: str, contract_type: str, status: str, current_page=None, page_number=None,
                                page_length=None):
    """
   获取合约爆仓单(非个人)
   :param symbol: 交易对
   :param contract_type:合约类型: this_week:当周 next_week:下周 quarter:季度
   :param status:状态 0：最近7天未成交 1:最近7天已成交
   :param current_page:当前页数索引值
   :param page_number:当前页数(使用page_number时current_page失效，current_page无需传)
   :param page_length:每页获取条数，最多不超过50
   :return:
   """
    # 校验参数
    if contract_type not in CONTRACT_TYPE:
        return PARAMS_ERROR
    if status not in ('0', '1'):
        return PARAMS_ERROR
    try:
        if current_page:
            current_page = int(current_page)
        if page_number:
            page_number = int(page_number)
        if page_length:
            page_length = int(page_length)
            if page_length > 50:
                return PARAMS_ERROR
    except Exception as e:
        logger.error(e)
        return PARAMS_ERROR

    okex_future = OKExFuture(api_key=API_KEY, secret_key=SECRET_KEY)

    return  await okex_future.future_explosive(symbol, contract_type, status, current_page, page_number, page_length)
