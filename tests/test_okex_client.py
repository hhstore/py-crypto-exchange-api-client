import logging
from pprint import pprint

from crypto_exchange.exchanges.okex.okex_rest.okex_spot_client import *

logger = logging.getLogger(__name__)


def test_spot_ticker():
    """
    获取OKEx币币行情
    symbol	String	是	币对如ltc_btc
    :return: is_ok:True/False
            status_code:200
            response:
            result: {'date': '1535945470' 返回数据时服务器时间,
                      'ticker': {'buy': '0.22306802' 买一价,
                                 'high': '0.22572930' 最高价,
                                 'last': '0.22337599' 最新成交价,
                                 'low': '0.22094114' 最低价,
                                 'sell': '0.22361779' 卖一价,
                                 'vol': '455.00000000' 成交量(最近的24小时)}})
    """
    data = okex_spot_ticker('ltc_eth')
    pprint(data)


def test_spot_depth():
    """
    获取OKEx币币市场深度
    symbol	String	是	币对如ltc_btc
    size	Integer	否(默认200)	value: 1-200
    :return: is_ok:True/False
            status_code:200
            response:
            result: {'asks': [[0.223344, 12.23304], [0.22334399, 2.6]],卖方深度
                    'bids': [[0.22255501, 1.5], [0.22246001, 8.1]]})买方深度
    """
    data = okex_spot_depth('ltc_eth', 2)
    pprint(data)


def test_spot_trades_info():
    """
    获取OKEx币币交易信息(60条)
    symbol	String	是	币对如ltc_btc
    since	Long	否(默认返回最近成交60条)	tid:交易记录ID(返回数据不包括当前tid值,最多返回60条数据)
    :return: is_ok:True/False
            status_code:200
            response:
            result:    [{'amount': 0.001717, 交易数量
                       'date': 1535934908, 交易时间
                       'date_ms': 1535934908879, 交易时间(ms)
                       'price': 0.22294284, 交易价格
                       'tid': 29794779, 交易生成ID
                       'type': 'sell'},] buy/sell
    """
    data = okex_spot_trades_info('ltc_eth')
    pprint(data)


def test_spot_k_line():
    """
    获取OKEx币币K线数据(每个周期数据条数2000左右)
    symbol	String	是	币对如ltc_btc
    type	String	是	1min/3min/5min/15min/30min/1day/3day/1week/1hour/2hour/4hour/6hour/12hour
    size	Integer	否(默认全部获取)	指定获取数据的条数
    since	Long	否(默认全部获取)	时间戳，返回该时间戳以后的数据(例如1417536000000)
    :return: is_ok:True/False
            status_code:200
            response:
            result: [[1535825820000, '0.2232721', '0.2232721', '0.2232721', '0.2232721', '0'],]
                    [时间戳，开，高，低，收，交易量]
    """
    data = okex_spot_k_line('ltc_eth', '1min')
    pprint(data)


def test_spot_user_info():
    """
    获取用户信息 访问频率 6次/2秒
    api_key	String	是	用户申请的apiKey
    sign	String	是	请求参数的签名
    :return: is_ok:True/False
            status_code:200
            response:
            result:{'info': {'funds': {'free': {'1st': '0.9985', 账户余额
                                                'aac': '0',},
                                    'freezed': {'1st': '0',     账户冻结余额
                                                'aac': '0',}}},
                   'result': True}
    """
    data = okex_spot_user_info()
    pprint(data)


def test_spot_trade():
    """
    下单交易 访问频率 20次/2秒
    api_key	String	是	用户申请的apiKey
    symbol	String	是	币对如ltc_btc
    type	String	是	买卖类型：限价单(buy/sell) 市价单(buy_market/sell_market)
    price	Double	否	下单价格 市价卖单不传price
    amount	Double	否	交易数量 市价买单不传amount,市价买单需传price作为买入总金额
    sign	String	是	请求参数的签名
    :return:is_ok:True/False
            status_code:200
            response:
            result: {'order_id': 6889183, 订单ID
                    'result': True}) 是否成功

                    {'error_code': 1002}) 错误返回
    """
    data = okex_spot_trade('1st_eth', 'buy', 0.00026500, 100)
    pprint(data)


def test_spot_batch_trade():
    """
    批量下单 访问频率 20次/2秒
    api_key	String	是	用户申请的apiKey
    symbol	String	是	币对如ltc_btc
    type	String	否	买卖类型：限价单(buy/sell)
    orders_data	String(格式[{price:3,amount:5,type:'sell'},{price:3,amount:3,type:'buy'}])
                            最大下单量为5， price和amount参数参考trade接口中的说明，
                            最终买卖类型由orders_data 中type 为准，
                            如orders_data不设定type 则由上面type设置为准。
    sign	String	是	请求参数的签名
    :return:is_ok:True/False
            status_code:200
            response:
            result: {'order_info': [{'order_id': 6891192}, {'order_id': 6891193}],
                    'result': True})
                      {'order_info': [{'order_id': 6891362}, {'errorCode': 1002, 'order_id': -1}],
                    'result': True})
                    {'error_code': 10008,
                     'result': False})

                    result:订单交易成功或失败
                    order_id:订单ID
                    只要其中任何一单下单成功就返回true
                    返回的订单信息和orders_data上传的订单顺序一致
                    如果下单失败：order_id为-1，error_code为错误代码
    """
    data = okex_spot_batch_trade('1st_eth',
                                 "[{price:0.00025000,amount:1,type:'buy'},"
                                 "{price:0.00025000,amount:1,type:'buy'}]", 'buy')
    pprint(data)


def test_spot_cancel_order():
    """
    撤销订单 访问频率 20次/2秒
    api_key	String	是	用户申请的apiKey
    symbol	String	是	币对如ltc_btc
    order_id	String	是	订单ID(多个订单ID中间以","分隔,一次最多允许撤消3个订单)
    sign	String	是	请求参数的签名

    :return:is_ok:True/False
            status_code:200
            response:
            result: true撤单请求成功，等待系统执行撤单；false撤单失败(用于单笔订单)
                    order_id:订单ID(用于单笔订单)
                    success:撤单请求成功的订单ID，等待系统执行撤单(用于多笔订单)
                    error:撤单请求失败的订单ID(用户多笔订单)
                    {'order_id': '6891884', 'result': True}
                    {'error': '', 'success': '6891999,6892000'})
                    {'error_code': 1009} 没有订单
    """
    data = okex_spot_cancel_order('1st_eth', '6891999')
    pprint(data)


def test_spot_order_info():
    """
    获取用户的订单信息 访问频率 20次/2秒(未成交)
    api_key	String	是	用户申请的apiKey
    symbol	String	是	币对如ltc_btc
    order_id	Long	是	订单ID -1:未完成订单，否则查询相应订单号的订单
    sign	String	是	请求参数的签名
    :return:is_ok:True/False
            status_code:200
            response:
            result:  {'orders': [{'amount': 1, 委托数量
                                  'avg_price': 0, 平均成交价
                                  'create_date': 1535953178000, 委托时间
                                  'deal_amount': 0, 成交数量
                                  'order_id': 6891630, 订单ID
                                  'orders_id': 6891630,
                                  'price': 0.00025, 委托价格
                                  'status': 0, -1:已撤销 0:未成交 1:部分成交 2:完全成交
                                                3:撤单处理中
                                  'symbol': '1st_eth', 交易对
                                  'type': 'buy'},], 交易类型
                    'result': True})
    """
    data = okex_spot_order_info('1st_eth', -1)
    pprint(data)


def test_spot_orders_info():
    """
    批量获取用户订单 访问频率 20次/2秒
    api_key	String	是	用户申请的apiKey
    type	Integer	是	查询类型 0:未完成的订单 1:已经完成的订单
    symbol	String	是	币对如ltc_btc
    order_id	String	是	订单ID(多个订单ID中间以","分隔,一次最多允许查询50个订单)
    sign	String	是	请求参数的签名
    :return:is_ok:True/False
            status_code:200
            response:
            result: {'orders': [{'amount': 1, 限价单请求：下单数量 /市价单请求：卖出的btc/ltc数量
                                  'avg_price': 0, 平均成交价
                                  'create_date': 1535953178000, 委托时间
                                  'deal_amount': 0, 成交数量
                                  'order_id': 6891630, 订单ID
                                  'orders_id': 6891630, 订单ID
                                  'price': 0.00025, 限价单请求：委托价格 /市价单请求：买入的usd金额
                                  'status': 0, -1:已撤销 0:未成交 1:部分成交
                                                        2:完全成交 4:撤单处理中
                                  'symbol': '1st_eth', 交易对
                                  'type': 'buy'}], 交易类型
                    'result': True} 结果信息
    """
    data = okex_spot_orders_info('1st_eth', '6891630,6891999', 0)
    pprint(data)


def test_spot_order_history():
    """
    获取历史订单信息，只返回最近两天的信息
    api_key	String	是	用户申请的apiKey
    symbol	String	是	币对如ltc_btc
    status	Integer	是	查询状态 0：未完成的订单 1：已经完成的订单(最近两天的数据)
    current_page	Integer	是	当前页数
    page_length	Integer	是	每页数据条数，最多不超过200
    sign	String	是	请求参数的签名
    :return:is_ok:True/False
            status_code:200
            response:
            result: {'currency_page': 1, 当前页码
                      'orders': [{'amount': 1, 委托数量
                                  'avg_price': 0, 平均成交价
                                  'create_date': 1535953178000, 委托时间
                                  'deal_amount': 0, 成交数量
                                  'order_id': 6891630, 订单ID
                                  'orders_id': 6891630,
                                  'price': 0.00025, 委托价格
                                  'status': 0, -1:已撤销 0:未成交 1:部分成交
                                                2:完全成交 4:撤单处理中
                                  'symbol': '1st_eth', 交易对
                                  'type': 'buy'},], 交易类型
                      'page_length': 20, 每页数据条数
                      'result': True, 代表成功返回
                      'total': 1}) 当前数据条数
    """
    data = okex_spot_order_history('1st_eth', 0, 1, 20)
    pprint(data)

# TODO 提币
# TODO 查询提币
# TODO 用户提现记录
# TODO 资金划转
# TODO 钱包信息
