import logging

from crypto_exchange.conf.exchange import Config
from crypto_exchange.exchanges.okex.okex_rest.okex_future import OKExFuture

logger = logging.getLogger(__name__)

API_KEY = Config.exchange_api_key['okex']['public_key']
SECRET_KEY = Config.exchange_api_key['okex']['secret_key']


def okex_future_ticker(symbol: str, contract_type):
    """
    获取合约行情数据
    :param symbol: 交易对
    :param contract_type: 合约类型
    :return: is_ok, status_code, response, result
    """
    # 校验参数
    okex_future = OKExFuture(api_key=API_KEY, secret_key=SECRET_KEY)
    result = okex_future.future_ticker(symbol, contract_type)
    return result


def okex_future_depth(symbol: str, contract_type: str, size: int, merge=0):
    """
    获取合约深度信息
    :param symbol: 交易对
    :param contract_type: 合约类型
    :param size: value
    :param merge: 合并深度
    :return:
    """
    # 校验参数
    okex_future = OKExFuture(api_key=API_KEY, secret_key=SECRET_KEY)
    result = okex_future.future_depth(symbol, contract_type, 200)
    return result


def okex_future_userinfo():
    """
    获取合约账户信息(全仓) 访问频率 10次/2秒
    :return:
    """
    # 校验参数
    okex_future = OKExFuture(api_key=API_KEY, secret_key=SECRET_KEY)
    result = okex_future.future_userinfo()
    return result


def okex_future_userinfo_4fix():
    """
    获取逐仓合约账户信息
    :return:
    """
    # 校验参数
    okex_future = OKExFuture(api_key=API_KEY, secret_key=SECRET_KEY)
    result = okex_future.future_userinfo_4fix()
    return result


def okex_future_position(symbol: str, contract_type: str):
    """
    获取合约全仓持仓信息 访问频率 10次/2秒
    :param symbol: 交易对
    :param contractType: 合约类型: this_week:当周 next_week:下周 quarter:季度
    :return:
    """
    # 校验参数
    okex_future = OKExFuture(api_key=API_KEY, secret_key=SECRET_KEY)
    result = okex_future.future_position(symbol, contract_type)
    return result


def okex_future_position_4fix(symbol: str, contract_type: str, type=None):
    """
    逐仓用户持仓查询 访问频率 10次/2秒
    :param symbol:交易对
    :param contract_type:合约类型: this_week:当周 next_week:下周 quarter:季度
    :param type:默认返回10倍杠杆持仓 type=1 返回全部持仓数据
    :return:
    """
    # 校验参数
    okex_future = OKExFuture(api_key=API_KEY, secret_key=SECRET_KEY)
    result = okex_future.future_position_4fix(symbol, contract_type, type=None)
    return result


def okex_future_trade(symbol: str, contract_type: str, price: str, amount: str, trade_type: str, match_price: str,
                      lever_rate: str):
    """
    合约下单 访问频率 5次/1秒(按币种单独计算)
    :param symbol:交易对
    :param contract_type:合约类型
    :param price:价格
    :param amount:委托数量
    :param trade_type:1:开多 2:开空 3:平多 4:平空
    :param match_price:是否为对手价 0:不是 1:是 ,当取值为1时,price无效
    :param lever_rate:杠杆倍数
    :return:
    """
    # 校验参数
    okex_future = OKExFuture(api_key=API_KEY, secret_key=SECRET_KEY)
    result = okex_future.future_trade(symbol, contract_type, price, amount, trade_type, match_price, lever_rate)
    return result


def okex_future_batch_trade(symbol: str, contract_type: str, orders_data: str, lever_rate: str):
    """
    合约批量下单 访问频率 3次/1秒 最多一次下1-5个订单（按币种单独计算）
    :param symbol: 交易对
    :param contract_type:合约类型: this_week:当周 next_week:下周 quarter:季度
    :param orders_data:JSON类型的字符串 例：[{price:5,amount:2,type:1,match_price:1},{price:2,amount:3,type:1,match_price:1}] 最大下单量为5，
    :param lever_rate:杠杆倍数
    :return:
    """
    # 校验参数
    okex_future = OKExFuture(api_key=API_KEY, secret_key=SECRET_KEY)
    result = okex_future.future_batch_trade(symbol, contract_type, orders_data, lever_rate)
    return result


def okex_future_cancel(symbol: str, contract_type: str, order_id: str):
    """
    取消合约订单 访问频率 2次/1秒，最多一次撤1-5个订单（按币种单独计算）
    :param symbol: 交易对
    :param contract_type: 合约类型: this_week:当周 next_week:下周 quarter:季度
    :param order_id: 订单ID(多个订单ID中间以","分隔,一次最多允许撤消5个订单)
    :return:
    """
    # 校验参数
    okex_future = OKExFuture(api_key=API_KEY, secret_key=SECRET_KEY)
    result = okex_future.future_cancel(symbol, contract_type, order_id)
    return result


def okex_future_trades_history(symbol: str, date: str, since: int):
    """
    获取合约交易历史(非个人) 访问频率 2次/2秒
    :param symbol: 交易对
    :param date: 合约交割时间，格式yyyy-MM-dd
    :param since:交易Id起始位置
    :return:
    """
    # 校验参数
    okex_future = OKExFuture(api_key=API_KEY, secret_key=SECRET_KEY)
    result = okex_future.future_trades_history(symbol, date, since)
    return result


# data = okex_future_trades_history('xrp', '2018-08-31',1535766266000)
# pprint(data)


def okex_future_order_info(symbol: str, contract_type: str, order_id: str, status: str, current_page: str,
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
    okex_future = OKExFuture(api_key=API_KEY, secret_key=SECRET_KEY)
    result = okex_future.future_order_info(symbol, contract_type, order_id, status, current_page, page_length)
    return result


def okex_future_orders_info(symbol: str, contract_type: str, orders_id: str):
    """
    批量获取合约订单信息
    :param symbol: 交易对
    :param contract_type:合约类型: this_week:当周 next_week:下周 quarter:季度
    :param order_id:订单ID(多个订单ID中间以","分隔,一次最多允许查询50个订单)
    :return:
    """
    # 校验参数
    okex_future = OKExFuture(api_key=API_KEY, secret_key=SECRET_KEY)
    result = okex_future.future_orders_info(symbol, contract_type, orders_id)
    return result


def okex_future_explosive(symbol: str, contract_type: str, status: str, current_page=None, page_number=None,
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
    okex_future = OKExFuture(api_key=API_KEY, secret_key=SECRET_KEY)
    result = okex_future.future_explosive(symbol, contract_type, status, current_page, page_number, page_length)
    return result
