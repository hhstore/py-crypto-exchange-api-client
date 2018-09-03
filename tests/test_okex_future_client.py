from pprint import pprint

from crypto_exchange.exchanges.okex.okex_rest.okex_future_client import *

logger = logging.getLogger(__name__)


def test_future_ticker():
    """
    GET 获取OKEx合约行情
    symbol	String	是	btc_usd ltc_usd eth_usd etc_usd bch_usd
    contract_type	String	是	合约类型: this_week:当周 next_week:下周 quarter:季度
    :return:is_ok:True/False
            status_code:200
            response:
            result:  {'date': '1535958172',
                      'ticker': {'buy': 0.337, 买一价
                                 'coin_vol': 0,
                                 'contract_id': 201809070150049, 合约ID
                                 'day_high': 0,
                                 'day_low': 0,
                                 'high': 0.352, 最高价
                                 'last': 0.338, 最新成交价
                                 'low': 0.335, 最低价
                                 'sell': 0.339, 卖一价
                                 'unit_amount': 10, 合约面值
                                 'vol': 478442}} 成交量(最近的24小时)
    """
    data = okex_future_ticker('xrp_usd', 'quarter')
    pprint(data)


def test_future_depth():
    """
    GET 获取OKEx合约深度信息
    symbol	String	是	btc_usd ltc_usd eth_usd etc_usd bch_usd
    contract_type	String	是	合约类型: this_week:当周 next_week:下周 quarter:季度
    size	Integer	是	value：1-200
    merge	Integer	否(默认0)	value：1(合并深度)
    :return: is_ok:True/False
            status_code:200
            response:
            result:  {'asks': [[0.339, 1469], [0.338, 2018], [0.337, 2503]],
                'bids': [[0.336, 3146], [0.335, 28512], [0.334, 390]]}

              合并深度 {'asks': [[0.36, 11715], [0.35, 31293], [0.34, 31288]],
                'bids': [[0.33, 47131], [0.32, 13755], [0.31, 276]]}
    """
    data = okex_future_depth('xrp', 'this_week', 3, 1)
    pprint(data)


def test_future_trades():
    """
    GET 获取OKEx合约交易记录信息
    symbol	String	是	btc_usd ltc_usd eth_usd etc_usd bch_usd
    contract_type	String	是	合约类型: this_week:当周 next_week:下周 quarter:季度
    :return:is_ok:True/False
            status_code:200
            response:
            result: [{'amount': 6, 交易数量
                   'date': 1535954253, 交易时间
                   'date_ms': 1535954253841, 交易时间(毫秒)
                   'price': 0.336, 交易价格
                   'tid': 1390559482839044, 交易ID
                   'type': 'buy'}, 交易类型
    """
    data = okex_future_trades('xrp', 'quarter')
    pprint(data)


def test_future_index():
    """
    GET 获取OKEx合约指数信息
    symbol	String	是	btc_usd ltc_usd eth_usd etc_usd bch_usd
    :return:is_ok:True/False
            status_code:200
            response:
            result: {'future_index': 0.336}
    """
    data = okex_future_index('xrp')
    pprint(data)


def test_future_estimated_price():
    """
    GET 获取交割预估价 交割预估价只有交割前三小时返回
    symbol	String	是	btc_usd ltc_usd eth_usd etc_usd bch_usd
    :return:is_ok:True/False
            status_code:200
            response:
            result: {'forecast_price': 0}
    """
    data = okex_future_estimated_price('xrp')
    pprint(data)


def test_future_k_line():
    """
    GET 获取OKEx合约K线信息
    symbol	String	是	btc_usd ltc_usd eth_usd etc_usd bch_usd
    type	String	是	1min/3min/5min/15min/30min/1day/3day/
                        1week/1hour/2hour/4hour/6hour/12hour
    contract_type	String	是	合约类型: this_week:当周 next_week:下周 quarter:季度
    size	Integer	否(默认0)	指定获取数据的条数
    since	Long	否(默认0)	时间戳（eg：1417536000000）。 返回该时间戳以后的数据
    :return:is_ok:True/False
            status_code:200
            response:
            result: [[1535788740000, 0.339, 0.339, 0.339, 0.339, 0, 0],]
                    时间戳，开，高，低，收，交易量，交易量转化BTC或LTC数量
    """
    data = okex_future_k_line('xrp', '12hour', 'quarter', 10)
    pprint(data)


def test_future_hold_amount():
    """
    GET 获取当前可用合约总持仓量
    symbol	String	是	btc_usd ltc_usd eth_usd etc_usd bch_usd
    contract_type	String	是	合约类型: this_week:当周 next_week:下周 quarter:季度
    :return:is_ok:True/False
            status_code:200
            response:
            result:[{'amount': 94876, 'contract_name': 'XRP0907'}]
                    总持仓量(张)，合约名
    """
    data = okex_future_hold_amount('xrp', 'this_week')
    pprint(data)


def test_future_price_limit():
    """
    GET 获取合约最高限价和最低限价
    symbol	String	是	btc_usd ltc_usd eth_usd etc_usd bch_usd
    contract_type	String	是	合约类型: this_week:当周 next_week:下周 quarter:季度
    :return: is_ok:True/False
            status_code:200
            response:
            result: {'high': 0.349, 'low': 0.328, 'usdCnyRate': 6.839}
                    最高买价,最低卖价,美元人民币汇率
    """
    data = okex_future_price_limit('xrp', 'this_week')
    pprint(data)


def test_future_user_info():
    """
    POST 获取OKEx合约账户信息(全仓) 访问频率 10次/2秒
    api_key	String	是	用户申请的apiKey
    sign	String	是	请求参数的签名
    :return:is_ok:True/False
            status_code:200
            response:
            result:  {'info': {'bch': {'account_rights': 0,
                                       'keep_deposit': 0,
                                       'profit_real': 0,
                                       'profit_unreal': 0,
                                       'risk_rate': 10000},
                                ......
                               'xrp': {'account_rights': 8.46516711, 账户权益
                                       'keep_deposit': 2.958579882, 保证金
                                       'profit_real': -0.01488095, 已实现盈亏
                                       'profit_unreal': -0.17610594, 未实行盈亏
                                       'risk_rate': 2.8612}}, 保证金率
                      'result': True})
    """
    data = okex_future_user_info()
    pprint(data)


def test_future_user_info_4fix():
    """
    POST 获取逐仓合约账户信息 访问频率 10次/2秒
    api_key	String	是	用户申请的apiKey
    sign	String	是	请求参数的签名
    :return:is_ok:True/False
            status_code:200
            response:
            result: {'error_code': 20022, 'interface': '/api/v1/future_userinfo', 'result': False}  接口调用错误（全仓模式调用全仓接口，逐仓模式调用逐仓接口）
                #TODO 逐仓返回值
    """
    data = okex_future_user_info_4fix()
    pprint(data)


def test_future_position():
    """
    POST 获取用户持仓获取OKEX合约账户信息 （全仓） 访问频率 10次/2秒
    symbol	String	是	btc_usd ltc_usd eth_usd etc_usd bch_usd
    contract_type	String	是	合约类型: this_week:当周 next_week:下周 quarter:季度
    api_key	String	是	用户申请的apiKey
    sign	String	是	请求参数的签名
    :return:is_ok:True/False
            status_code:200
            response:
            result:  {'force_liqu_price': '0.469', 预估爆仓价
                      'holding': [{'buy_amount': 0, 多仓数量
                                   'buy_available': 0, 多仓可平仓数量
                                   'buy_price_avg': 0, 开仓平均价
                                   'buy_price_cost': 0, 结算基准价
                                   'buy_profit_real': -0.00744048, 多仓已实现盈余
                                   'contract_id': 201809070150049, 合约id
                                   'contract_type': 'this_week', 合约类型
                                   'create_date': 1535766266000, 创建日期
                                   'lever_rate': 10, 杠杆倍数
                                   'sell_amount': 1, 空仓数量
                                   'sell_available': 1, 空仓可平仓数量
                                   'sell_price_avg': 0.336, 开仓平均价
                                   'sell_price_cost': 0.336, 结算基准价
                                   'sell_profit_real': -0.00744048, 空仓已实现盈余
                                   'symbol': 'xrp_usd'}], 交易对
                      'result': True})
    """
    data = okex_future_position('xrp', 'this_week')
    pprint(data)


def test_future_position_4fix():
    """
    POST 逐仓用户持仓查询 访问频率 10次/2秒
    symbol	String	是	btc_usd ltc_usd eth_usd etc_usd bch_usd
    contract_type	String	是	合约类型: this_week:当周 next_week:下周 quarter:季度
    api_key	String	是	用户申请的apiKey
    sign	String	是	请求参数的签名
    type	String	否	默认返回10倍杠杆持仓 type=1 返回全部持仓数据
    :return:is_ok:True/False
            status_code:200
            response:
            result:
             {'error_code': 20022, 'interface': '/api/v1/future_position', 'result': False}
             # TODO 逐仓返回值
    """
    data = okex_future_position_4fix('xrp', 'this_week')
    pprint(data)


def test_future_trade():
    """
    POST 合约下单 访问频率 5次/1秒(按币种单独计算)
    symbol	String	是	btc_usd ltc_usd eth_usd etc_usd bch_usd
    contract_type	String	是	合约类型: this_week:当周 next_week:下周 quarter:季度
    api_key	String	是	用户申请的apiKey
    sign	String	是	请求参数的签名
    price	String	是	价格
    amount	String	是	委托数量（张）
    trade_type	String	是	1:开多 2:开空 3:平多 4:平空
    match_price	String	否	是否为对手价 0:不是 1:是 ,当取值为1时,price无效
    lever_rate	String	否	杠杆倍数，下单时无需传送，系统取用户在页面上设置的杠杆倍数。
                            且“开仓”若有10倍多单，就不能再下20倍多单
    :return: is_ok:True/False
            status_code:200
            response:
            result:  {'order_id': 1391235616674816, 'result': True})
                     {'error_code': 20012, 'result': False}
                    10倍/20倍杠杆开BTC后保证金率低于90%/80%，10倍/20倍杠杆开LTC后保证金率低于80%/60%
    """
    data = okex_future_trade('xrp', 'this_week', '0.320', '1', '1', '0', '10')
    pprint(data)


def test_future_batch_trade():
    """
    POST 批量下单 访问频率 3次/1秒 最多一次下1-5个订单（按币种单独计算）
    api_key	String	是	用户申请的apiKey
    symbol	String	是	btc_usd ltc_usd eth_usd etc_usd bch_usd
    contract_type	String	是	合约类型: this_week:当周 next_week:下周 quarter:季度
    orders_data	String	是	JSON类型的字符串
                            例：[{price:5,amount:2,type:1,match_price:1},]
                            最大下单量为5，
                            price,amount,type,match_price参数参考future_trade接口中的说明
    sign	String	是	请求参数的签名
    lever_rate	String	否	杠杆倍数，下单时无需传送，系统取用户在页面上设置的杠杆倍数。
                            且“开仓”若有10倍多单，就不能再下20倍多单
    :return: is_ok:True/False
            status_code:200
            response:
            result:  {'order_info': [{'order_id': 1391285256008704},
                                     {'error_code': 20012, 'order_id': -1}],
                      'result': True})
                      只要其中任何一单下单成功就返回true
                      返回的结果数据和orders_data提交订单数据顺序一致
                      如果下单失败：order_id为-1，error_code为错误代码
    """
    data = okex_future_batch_trade('xrp', 'this_week',
                                   '[{price:0.320,amount:1,type:1,match_price:0},'
                                   '{price:0.310,amount:1,type:1,match_price:0}]', '10')
    pprint(data)


def test_future_cancel():
    """
    POST 取消合约订单 访问频率 2次/1秒，最多一次撤1-5个订单（按币种单独计算）
    api_key	String	是	用户申请的apiKey
    symbol	String	是	btc_usd ltc_usd eth_usd etc_usd bch_usd
    order_id	String	是	订单ID(多个订单ID中间以","分隔,一次最多允许撤消5个订单)
    sign	String	是	请求参数的签名
    contract_type	String	是	合约类型: this_week:当周 next_week:下周 quarter:季度
    :return:is_ok:True/False
            status_code:200
            response:
            result: {'order_id': '1391285256008704', 'result': True}
                     {'error_code': 20015, 'result': False} 订单信息不存在
    """
    data = okex_future_cancel('xrp', 'this_week', '1391285256008705')
    pprint(data)


def test_future_trades_history():
    """
    POST 获取OKEX合约交易历史（非个人）访问频率 访问频率 2次/2秒
    api_key	String	是	用户申请的apiKey
    sign	String	是	请求参数的签名
    symbol	String	是	btc_usd ltc_usd eth_usd etc_usd bch_usd
    date	String	是	合约交割时间，格式yyyy-MM-dd
    since	Long	是	交易Id起始位置
    :return:is_ok:True/False
            status_code:200
            response:
            result:  {'error_code': 20007, 'result': False} 参数错误
                    {"result":false,"error_code":20049} 用户请求接口过于频繁
                    [{'amount': '5', 交易数量
                       'date': 1535965349000, 交易时间(毫秒)
                       'price': '0.33', 交易价格
                       'tid': 1391286666690561, 交易ID
                       'type': 'sell'}, 交易类型（buy/sell）

    """
    data = okex_future_trades_history('xrp', '2018-09-07', 1391285256008705)
    pprint(data)


def test_future_order_info():
    """
    POST 获取合约订单信息
    symbol	String	是	btc_usd ltc_usd eth_usd etc_usd bch_usd
    contract_type	String	是	合约类型: this_week:当周 next_week:下周 quarter:季度
    api_key	String	是	用户申请的apiKey
    sign	String	是	请求参数的签名
    status	String	否	查询状态 1:未完成的订单 2:已经完成的订单
    order_id	String	是	订单ID -1:查询指定状态的订单，否则查询相应订单号的订单
    current_page	String	否	当前页数
    page_length	String	否	每页获取条数，最多不超过50
    :return: is_ok:True/False
            status_code:200
            response:
            result:{'orders':[{'amount': 1, 委托数量
                          'contract_name': 'XRP0907', 合约名称
                          'create_date': 1535965328000, 委托时间
                          'deal_amount': 0, 成交数量
                          'fee': 0, 手续费
                          'lever_rate': 10, 杠杆倍数  value:10\20  默认10
                          'order_id': 1391285256008704, 订单ID
                          'price': 0.32, 订单价格
                          'price_avg': 0, 平均价格
                          'status': -1, 订单状态
                                    (0等待成交 1部分成交 2全部成交 -1撤单 4撤单处理中 5撤单中)
                          'symbol': 'xrp_usd', 交易对
                          'type': 1, 订单类型 1：开多 2：开空 3：平多 4： 平空
                          'unit_amount': 10},], 合约面值
                  'result': True}
                  {'orders': [], 'result': True}
    """
    data = okex_future_order_info('xrp', 'this_week', '-1', '2', '1', '20')
    pprint(data)


def test_future_orders_info():
    """
    POST 批量获取合约订单信息
    symbol	String	是	btc_usd ltc_usd eth_usd etc_usd bch_usd
    contract_type	String	是	合约类型: this_week:当周 next_week:下周 quarter:季度
    api_key	String	是	用户申请的apiKey
    sign	String	是	请求参数的签名
    order_id	String	是	订单ID(多个订单ID中间以","分隔,一次最多允许查询50个订单)
    :return:is_ok:True/False
            status_code:200
            response:
            result:  {'orders': [{'amount': 1, 委托数量
                                  'contract_name': 'XRP0907', 合约名称
                                  'create_date': 1535767128000, 委托时间
                                  'deal_amount': 1, 成交数量
                                  'fee': -0.01488095, 手续费
                                  'lever_rate': 10, 杠杆倍数  value:10\20  默认10
                                  'order_id': 1378296031683584, 订单ID
                                  'price': 0.333, 订单价格
                                  'price_avg': 0.336, 平均价格
                                  'status': 2, 订单状态
                                           (0等待成交 1部分成交 2全部成交 -1撤单 4撤单处理中)
                                  'symbol': 'xrp_usd', 交易对
                                  'type': 2, 订单类型 1：开多 2：开空 3：平多 4： 平空
                                  'unit_amount': 10},], 合约面值
                      'result': True})
    """
    data = okex_future_orders_info('xrp', 'this_week', '1378296031683584,1391235616674816,1391285256008704')
    pprint(data)


def test_future_explosive():
    """
    POST 获取合约爆仓单(非个人)
    api_key	String	是	用户申请的apiKey
    sign	String	是	请求参数的签名
    symbol	String	是	btc_usd ltc_usd eth_usd etc_usd bch_usd
    contract_type	String	是	合约类型: this_week:当周 next_week:下周 quarter:季度
    status	String	是	状态 0：最近7天未成交 1:最近7天已成交
    current_page	Integer	否	当前页数索引值
    page_number	Integer	否	当前页数(使用page_number时current_page失效，current_page无需传)
    page_length	Integer	否	每页获取条数，最多不超过50
    :return:is_ok:True/False
            status_code:200
            response:
            result: {'data': []}
                     {'data': [{'amount': '646', 委托数量（张）
                                'create_date': '2018-09-03 18:06:23', 创建时间
                                'loss': '0', 穿仓用户亏损
                                'price': '0.331', 委托价格
                                'type': 3},]}) 交易类型
                                1：买入开多 2：卖出开空 3：卖出平多 4：买入平空

    """
    data = okex_future_explosive('xrp', 'this_week', '1', '1', '1', '20')
    pprint(data)
