from pprint import pprint

import pytest

from crypto_exchange.exchanges.okex.okex_rest.okex_spot_client import *

logger = logging.getLogger(__name__)


@pytest.mark.asyncio
async def test_spot_ticker():
    """
    GET 获取OKEx币币行情
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
    data = (okex_spot_ticker(API_KEY, SECRET_KEY, 'ltc_eth') for i in range(4))

    for item in data:
        pprint(await item)
    pprint(data)

    """
 {'date': '1536050174',
  'ticker': {'buy': '0.23254200',
             'high': '0.23357520',
             'last': '0.23357499',
             'low': '0.22397702',
             'sell': '0.23357500',
             'vol': '1016.00000000'}})
 {'date': '1536050174',
  'ticker': {'buy': '0.23254200',
             'high': '0.23357520',
             'last': '0.23357499',
             'low': '0.22397702',
             'sell': '0.23357500',
             'vol': '1016.00000000'}})
 {'date': '1536050176',
  'ticker': {'buy': '0.23254200',
             'high': '0.23357520',
             'last': '0.23357499',
             'low': '0.22397702',
             'sell': '0.23357500',
             'vol': '1016.00000000'}})
 {'date': '1536050177',
  'ticker': {'buy': '0.23254200',
             'high': '0.23357520',
             'last': '0.23357499',
             'low': '0.22397702',
             'sell': '0.23357500',
             'vol': '1016.00000000'}})
 {'date': '1536050178',
  'ticker': {'buy': '0.23254200',
             'high': '0.23357520',
             'last': '0.23357499',
             'low': '0.22397702',
             'sell': '0.23357500',
             'vol': '1016.00000000'}})
 {'date': '1536050179',
  'ticker': {'buy': '0.23254200',
             'high': '0.23357520',
             'last': '0.23357499',
             'low': '0.22397702',
             'sell': '0.23357500',
             'vol': '1016.00000000'}})
    """


@pytest.mark.asyncio
async def test_spot_depth():
    """
    GET 获取OKEx币币市场深度
    symbol	String	是	币对如ltc_btc
    size	Integer	否(默认200)	value: 1-200
    :return: is_ok:True/False
            status_code:200
            response:
            result: {'asks': [[0.223344, 12.23304], [0.22334399, 2.6]],卖方深度
                    'bids': [[0.22255501, 1.5], [0.22246001, 8.1]]})买方深度
    """
    data = await okex_spot_depth(API_KEY, SECRET_KEY, 'ltc_eth', 2)
    pprint(data)


@pytest.mark.asyncio
async def test_spot_trades_info():
    """
    GET 获取OKEx币币交易信息(60条)
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
    data = await okex_spot_trades_info(API_KEY, SECRET_KEY, 'ltc_eth')
    pprint(data)


@pytest.mark.asyncio
async def test_spot_k_line():
    """
    GET 获取OKEx币币K线数据(每个周期数据条数2000左右)
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
    data = await okex_spot_k_line(API_KEY, SECRET_KEY, 'ltc_eth', '1min')
    pprint(data)


@pytest.mark.asyncio
async def test_spot_user_info():
    """
    POST 获取用户信息 访问频率 6次/2秒
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
    data = await okex_spot_user_info(API_KEY, SECRET_KEY, )
    pprint(data)


@pytest.mark.asyncio
async def test_spot_place_order():
    """
    POST 下单交易 访问频率 20次/2秒
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
                    'result': True} 是否成功

                    {'error_code': 1002} 交易金额大于余额
    """
    # data = await okex_spot_trade('1st_eth', 'buy', 0.00000500, 100)
    data = await okex_spot_place_order(API_KEY, SECRET_KEY, '1st_eth', 'buy', 0.00000500, 100)
    pprint(data)
    # pprint(data)


@pytest.mark.asyncio
async def test_spot_batch_trade():
    """
    POST 批量下单 访问频率 20次/2秒
    api_key	String	是	用户申请的apiKey
    symbol	String	是	币对如ltc_btc
    orders_data	String(格式[{price:3,amount:5,type:'sell'},{price:3,amount:3,type:'buy'}])
                            最大下单量为5， price和amount参数参考trade接口中的说明，
                            最终买卖类型由orders_data 中type 为准，
                            如orders_data不设定type 则由上面type设置为准。
    type	String	否	买卖类型：限价单(buy/sell)
    sign	String	是	请求参数的签名
    :return:is_ok:True/False
            status_code:200
            response:
            result: {'order_info': [{'order_id': 6891192}, {'order_id': 6891193}],
                    'result': True})
                      {'order_info': [{'order_id': 6891362}, {'errorCode': 1002, 'order_id': -1}],
                    'result': True})
                    {'error_code': 10008,'result': False})

                    result:订单交易成功或失败
                    order_id:订单ID
                    只要其中任何一单下单成功就返回true
                    返回的订单信息和orders_data上传的订单顺序一致
                    如果下单失败：order_id为-1，error_code为错误代码
    """
    data = await okex_spot_batch_trade(API_KEY, SECRET_KEY, '1st_eth',
                                       "[{price:0.00025000,amount:1,type:'buy'},"
                                       "{price:0.00025000,amount:1,type:'buy'}]", 'buy')
    pprint(data)


@pytest.mark.asyncio
async def test_spot_cancel_order():
    """
    POST 撤销订单 访问频率 20次/2秒
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
    data = await okex_spot_cancel_order(API_KEY, SECRET_KEY, '1st_eth', '6891999')
    pprint(data)


@pytest.mark.asyncio
async def test_spot_order_info():
    """
    POST 获取用户的订单信息 访问频率 20次/2秒(未成交)
    api_key	String	是	用户申请的apiKey
    symbol	String	是	币对如ltc_btc
    order_id	Long	是	订单ID -1:未完成订单(负数都可以)，否则查询相应订单号的订单
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
    data = await okex_spot_order_info(API_KEY, SECRET_KEY, '1st_eth', -1)
    pprint(data)


@pytest.mark.asyncio
async def test_spot_orders_info():
    """
    POST 批量获取用户订单 访问频率 20次/2秒
    api_key	String	是	用户申请的apiKey
    symbol	String	是	币对如ltc_btc
    order_id	String	是	订单ID(多个订单ID中间以","分隔,一次最多允许查询50个订单)
    type	Integer	是	查询类型 0:未完成的订单 1:已经完成的订单
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
    data = await okex_spot_orders_info(API_KEY, SECRET_KEY, '1st_eth', '6891630,6891999', 0)
    pprint(data)


@pytest.mark.asyncio
async def test_spot_order_history():
    """
    POST 获取历史订单信息，只返回最近两天的信息
    api_key	String	是	用户申请的apiKey
    symbol	String	是	币对如ltc_btc
    status	Integer	是	查询状态 0：未完成的订单 1：已经完成的订单(最近两天的数据)
    current_page	Integer	是	当前页数 (小于等于1都显示首页)
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
    data = await okex_spot_order_history(API_KEY, SECRET_KEY, '1st_eth', 0, 1, 10)
    pprint(data)


@pytest.mark.asyncio
async def test_withdraw():
    """
    POST 提币BTC/LTC/ETH/ETC/BCH
    api_key	String	是	用户申请的apiKey
    symbol	String	是	币对如ltc_usd
    chargefee	Double	是	网络手续费 >=0 BTC范围 [0.002，0.005]
    LTC范围 [0.001，0.2] ETH范围 [0.01] ETC范围 [0.0001，0.2] BCH范围 [0.0005，0.002] 手续费越高，网络确认越快，向OKCoin提币设置为0
    trade_pwd	String	是	交易密码
    withdraw_address	String	是	认证的地址、邮箱或手机号码
    withdraw_amount	Double	是	提币数量 BTC>=0.01 LTC>=0.1 ETH>=0.1 ETC>=0.1 BCH>=0.1
    target	String	是	地址类型 okcn：国内站 okcom：国际站 okex：OKEX address：外部地址
    sign	String	是	请求参数的签名
    :return:is_ok:True/False
            status_code:200
            response:
            result: # TODO 提币返回值
                {"withdraw_id":301,"result":true}
                提币申请ID，true表示请求成功
    """
    data = await okex_withdraw(API_KEY, SECRET_KEY)
    pprint(data)


@pytest.mark.asyncio
async def test_cancel_withdraw():
    """
    POST 取消提币BTC/LTC/ETH/ETC/BCH
    api_key	String	是	用户申请的apiKey
    symbol	String	是	币对如ltc_usd
    withdraw_id	String	是	提币申请Id
    sign	String	是	请求参数的签名
    :return:is_ok:True/False
            status_code:200
            response:
            result:# TODO 取消提币返回值
                    withdraw_id:提币申请Id
                    result:true表示请求成功
    """
    data = await okex_cancel_withdraw(API_KEY, SECRET_KEY, )
    pprint(data)


@pytest.mark.asyncio
async def test_withdraw_info():
    """
    POST 查询提币BTC/LTC/ETH/ETC/BCH信息
    api_key	String	是	用户申请的apiKey
    symbol	String	是	币对如ltc_usd
    withdraw_id	String	是	提币申请Id
    sign	String	是	请求参数的签名
    :return:is_ok:True/False
            status_code:200
            response:
            result: # TODO 查询提币返回值
                    result:true表示请求成功
                    address:提现地址
                    amount:提现金额
                    created_date:提现时间
                    chargefee:网络手续费
                    status:提现状态（-3:撤销中;-2:已撤销;-1:失败;0:等待提现;1:提现中;2:已汇出;3:邮箱确认;4:人工审核中5:等待身份认证）
                    withdraw_id:提币申请Id
    """
    data = await okex_withdraw_info(API_KEY, SECRET_KEY, )
    pprint(data)


@pytest.mark.asyncio
async def test_account_records():
    """
    POST 获取用户提现/充值记录
    api_key	String	是	用户申请的apiKey
    symbol	String	是	币种如btc_usd, ltc_usd, eth_usd, etc_usd, bch_usd, usdt_usd
    type	Integer	是	0：充值 1 ：提现
    current_page	Integer	是	当前页数
    page_length	Integer	是	每页数据条数，最多不超过50
    sign	String	是	请求参数的签名
    :return:is_ok:True/False
            status_code:200
            response:
            result: # TODO 用户提现记录返回值
                    {'records': [], 'result': True, 'symbol': 'btc'}
                    {'error_code': 10012, 'result': False} 10012当前网站暂时只支持btc_usd ltc_usd
                    addr: 地址
                    account: 账户名称
                    amount: 金额
                    bank: 银行
                    benificiary_addr: 收款地址
                    transaction_value: 提现扣除手续费后金额
                    fee: 手续费
                    date: 时间
                    symbol: btc, ltc, eth, etc, bch, usdt
                    status: 记录状态,如果查询充值记录:(-1:充值失败;0:等待确认;1:充值成功),
                    如果查询提现记录:(-3:撤销中;-2:已撤销;-1:失败;0:等待提现;
                                1:提现中;2:已汇出;3:邮箱确认;4:人工审核中;5:等待身份认证)
    """
    data = await okex_account_records(API_KEY, SECRET_KEY, 'eth', 1, 1, 20)
    pprint(data)


@pytest.mark.asyncio
async def test_funds_transfer():
    """
    POST 资金划转
    api_key	String	是	用户申请的apiKey
    symbol	String	是	btc_usd ltc_usd eth_usd etc_usd bch_usd
    amount	Number	是	划转数量
    from	Number	是	转出账户(1：币币账户 3：合约账户 6：我的钱包)
    to	    Number  是  转入账户(1：币币账户 3：合约账户 6：我的钱包)
    sign	String	是	请求参数的签名
    :return: is_ok:True/False
            status_code:200
            response:
            result: #
                     {'records': [], 'result': True, 'symbol': 'eth'}
                     {'result': True, 'symbol': 'eth'}
                    result:划转结果。若是划转失败，将给出错误码提示。
                    {'records': [{'addr': '0xa3a7d25203dde12b30f9bfbc9f5edcc76b0ff737',
                                   'amount': 0.03,
                                   'date': 1535544985000,
                                   'fee': 0,
                                   'status': 2}],
                      'result': True,
                      'symbol': 'eth'}
    """
    data = await okex_funds_transfer(API_KEY, SECRET_KEY, 'eth_usd', 0, 1, 6)
    pprint(data)


@pytest.mark.asyncio
async def test_wallet_info():
    """
    POST 获取用户钱包账户信息 访问频率 6次/2秒
    api_key	String	是	用户申请的apiKey
    sign	String	是	请求参数的签名
    :return: is_ok:True/False
            status_code:200
            response:
            result: free:账户余额
                    holds:账户锁定余额
                    {'info': {'funds': {'free': {'1st': '0',
                                                  'aac': '0',
                                                  'xmr': '0',
                                                  'xrp': '0.0000000000000000',
                                                  'zil': '0',
                                                  'zip': '0',
                                                  'zrx': '0'},
                                         'holds': {'1st': '0',
                                                   'xmr': '0',
                                                   'xrp': '0.0000000000000000',
                                                   'zip': '0',
                                                   'zrx': '0'}}},
                    'result': True}
    """
    data = await okex_wallet_info(API_KEY, SECRET_KEY, )
    pprint(data)
