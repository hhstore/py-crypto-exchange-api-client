import base64
import datetime
import hashlib
import hmac
import json
import urllib
from pprint import pprint

import logging

import requests

from crypto_exchange.exchanges.huobi.huobi_rest.huobi_rest_client import *

logger = logging.getLogger(__name__)


def test_history_k_line():
    """
    GET 获取K线数据
    symbol	true string	交易对	btcusdt, bchbtc, rcneth ...
    period	true string	K线类型	1min, 5min, 15min, 30min, 60min, 1day, 1mon, 1week, 1year
    size	false integer 获取数量 150	[1,2000]
    :return:is_ok:True/False
            status_code:200
            response:
            result:    {'ch': 'market.bchbtc.kline.1min', 数据所属的 channel，格式： market.$symbol.kline.$period
                        'data': [{'amount': 0.0074, 成交量
                                'close': 0.08633, 收盘价，当K线为最晚的一根时，是最新成交价
                                'count': 1, 成交笔数
                                'high': 0.08633, 最高价
                                'id': 1536046560, K线id
                                'low': 0.08633, 最低价
                                'open': 0.08633, 开盘价
                                'vol': 0.000638842}], 成交额
                        'status': 'ok', 请求处理结果
                        'ts': 1536046605559}) 响应生成时间点，单位：毫秒
                        period=not-exist
                        {
                          "ts": 1490758171271,
                          "status": "error",
                          "err-code": "invalid-parameter",
                          "err-msg": "invalid period"
                        }
                        size=not-exist
                        {
                          "ts": 1490758221221,
                          "status": "error",
                          "err-code": "bad-request",
                          "err-msg": "invalid size, valid range: [1,2000]"
                        }
                        symbol=not-exist
                        {
                          "ts": 1490758171271,
                          "status": "error",
                          "err-code": "invalid-parameter",
                          "err-msg": "invalid symbol"
                        }

    """
    data = huobi_history_k_line('bchbtc', '1min', 1)
    pprint(data)


def test_detail_merged():
    """
    GET 获取聚合行情(Ticker)
    symbol	true	string	交易对		btcusdt, bchbtc, rcneth ...
    :return:is_ok:True/False
            status_code:200
            response:
            result: {'ch': 'market.btcusdt.detail.merged', 数据所属的 channel，格式： market.$symbol.detail.merged
                  'status': 'ok', 请求处理结果
                  'tick': {'amount': 17845.70984869188, 成交量
                           'ask': [7325.9, 0.3], [卖1价,卖1量]
                           'bid': [7325.66, 0.043], [买1价,买1量]
                           'close': 7325.66, 收盘价,当K线为最晚的一根时，是最新成交价
                           'count': 70705, 成交笔数
                           'high': 7336.2, 最高价
                           'id': 18577753224, K线id
                           'low': 7213.76, 最低价
                           'open': 7263.3, 开盘价
                           'version': 18577753224, # TODO
                           'vol': 129763707.9717842}, 成交额
                  'ts': 1536048054139}) 响应生成时间点，单位：毫秒

                  {
                      "ts": 1490758171271,
                      "status": "error",
                      "err-code": "invalid-parameter",
                      "err-msg": "invalid symbol”
                    }
    """
    data = huobi_detail_merged('btcusdt')
    pprint(data)


def test_tickers():
    """
    GET 获取行情数据 传参返回64条,150条。。。 不传参返回280条，281条。。。
    symbol	false	string	交易对		btcusdt, bchbtc, rcneth ...

    :return: {'data': [{'amount': 144314.8845497147, 24小时成交量
                        'close': 0.002426, 日K线 收盘价
                        'count': 4559, 24小时成交笔数
                        'high': 0.002525, 日K线 最高价
                        'low': 0.0024, 日K线 最低价
                        'open': 0.002478, 日K线 开盘价
                        'symbol': 'iotaeth', 交易对
                        'vol': 357.0596689291}, 24小时成交额

                       {'amount': 43263919.249359325,
                        'close': 0.017,
                        'count': 7741,
                        'high': 0.019799,
                        'low': 0.016586,
                        'open': 0.019244,
                        'symbol': 'vetusdt',
                        'vol': 806576.241574161}],
              'status': 'ok',
              'ts': 1536147522382}


                        'amount': 28845.376782780888,
                        'close': 0.00042066,
                        'count': 764,
                        'high': 0.00045185,
                        'low': 0.00040098,
                        'open': 0.00045057,
                        'symbol': 'hcbtc',
                        'vol': 12.652213953055},
    """
    data = huobi_tickers()
    pprint('=====')
    pprint(len(data[3]['data']))
    pprint(data[3]['data'])


def test_depth():
    """
    GET 获取 Market Depth 数据
    symbol	true	string	交易对		btcusdt, bchbtc, rcneth ...
    type	true	string	Depth 类型   step0, step1, step2, step3, step4, step5（合并深度0-5）；
                                        step0时，不合并深度
    用户选择“合并深度”时，一定报价精度内的市场挂单将予以合并显示。合并深度仅改变显示方式，不改变实际成交价格
                                        150条，20条，20条，20条，13条，2条

    :return: {'ch': 'market.bchbtc.depth.step1', 数据所属的 channel
              'status': 'ok',
              'tick': {'asks': [[0.07966, 0.0168], 卖盘,[price(成交价), amount(成交量)], 按price升序
                                [0.07974, 178.163],
                                [0.07995, 0.0312],
                                [0.08005, 3.6491]],
                       'bids': [[0.07881, 2.3321], 买盘,[price(成交价), amount(成交量)], 按price降序
                                [0.07793, 1.2831],
                                [0.0779, 8.0],
                                [0.07786, 1.0101]],
                       'ts': 1536197634024,
                       'version': 18790857597},
              'ts': 1536197634142} 消息生成时间，单位：毫秒
    """
    data = huobi_depth('bchbtc', 'step0')
    pprint(data)
    pprint(len(data[3]['tick']['asks']))


def test_trade_detail():
    """
    GET 获取 Trade Detail 数据
    symbol	true	string	交易对		btcusdt, bchbtc, rcneth ...

    :return: {'ch': 'market.bchbtc.trade.detail',
              'status': 'ok',
              'tick': {'data': [{'amount': 0.0122, 成交量
                                 'direction': 'buy', 主动成交方向
                                 'id': 1879244149411761619636, 成交id
                                 'price': 0.07894, 成交价钱
                                 'ts': 1536198604559}], 成交时间
                       'id': 18792441494, 消息id
                       'ts': 1536198604559}, 最新成交时间
              'ts': 1536198607247}
    """
    data = huobi_trade_detail('bchbtc')
    pprint(data)


def test_history_trade():
    """
    GET 批量获取最近的交易记录
    symbol	true	string	交易对		btcusdt, bchbtc, rcneth ...
    size	false	integer	获取交易记录的数量	1	[1, 2000]

    :return:      {'ch': 'market.bchbtc.trade.detail', 数据所属的 channel
                  'data': [{'data': [{'amount': 0.4131, 成交量
                                      'direction': 'sell', 主动成交方向
                                      'id': 1879413666211762700805, 成交id
                                      'price': 0.079023, 成交价
                                      'ts': 1536199618475}], 成交时间
                            'id': 18794136662, 消息id
                            'ts': 1536199618475}, 最新成交时间

                           {'data': [{'amount': 9.806,
                                      'direction': 'buy',
                                      'id': 1879409273011762671498,
                                      'price': 0.07906,
                                      'ts': 1536199594395}],
                            'id': 18794092730,
                            'ts': 1536199594395}],
                  'status': 'ok',
                  'ts': 1536199622489} 发送时间
    """
    data = huobi_history_trade('bchbtc', 2)
    pprint(data)


def test_trade_24_detail():
    """
    获取 Market Detail 24小时成交量数据
    symbol	true	string	交易对		btcusdt, bchbtc, rcneth ...

    :return:  {'ch': 'market.bchbtc.detail',
              'status': 'ok',
              'tick': {'amount': 14349.3589, 24小时成交量
                       'close': 0.07897, 当前成交价
                       'count': 14432, 近24小时累积成交数
                       'high': 0.085659, 近24小时最高价
                       'id': 18795055125, 消息id
                       'low': 0.076188, 近24小时最低价
                       'open': 0.085058, 前推24小时成交价
                       'version': 18795055125,
                       'vol': 1151.9808346516}, 近24小时累积成交额
              'ts': 1536200177391}
    """
    data = huobi_trade_24_detail('bchbtc')
    pprint(data)


def test_symbols():
    """
    默认 查询Pro站支持的所有交易对及精度
    查询HADAX站支持的所有交易对及精度
    site	false	string	查询站	hadax

    :return:  {'data': None,
              'err-code': 'api-signature-not-valid',
              'err-msg': 'Signature not valid: Verification failure [校验失败]',
              'status': 'error'}

            284  {'data': [{'amount-precision': 4, 数量精度位数（0为个位，注意不是交易限额）
                        'base-currency': 'btc', 基础币种
                        'price-precision': 2, 价格精度位数（0为个位)
                        'quote-currency': 'usdt', 计价币种
                        'symbol': 'btcusdt', 交易对
                        'symbol-partition': 'main'}, 交易区  main主区，innovation创新区，bifurcation分叉区
                        {'amount-precision': 2,
                        'base-currency': 'ncash',
                        'price-precision': 10,
                        'quote-currency': 'btc',
                        'symbol': 'ncashbtc',
                        'symbol-partition': 'innovation'}],
              'status': 'ok'})

            88  {'data': [{'amount-precision': 2,
                        'base-currency': 'ncc',
                        'price-precision': 10,
                        'quote-currency': 'btc',
                        'symbol': 'nccbtc',
                        'symbol-partition': 'hadax'},
                       {'amount-precision': 2,
                        'base-currency': 'rte',
                        'price-precision': 10,
                        'quote-currency': 'btc',
                        'symbol': 'rtebtc',
                        'symbol-partition': 'hadax'}],
              'status': 'ok'}
    """
    data = huobi_symbols()
    pprint(data)
    pprint(len(data[3]['data']))


def test_currency():
    """
    默认 查询Pro站支持的所有币种
    查询HADAX站支持的所有币种
    site	false	string	查询站	hadax

    :return:130  {'data': ['hb10',
                           'usdt',
                           'btc',
                           'ncash'],
                 'status': 'ok'}

            59   {'data': ['usdt',
                           'btc',
                           'eth',
                           'rte'],
                 'status': 'ok'}
    """
    data = huobi_currency()
    pprint(data)
    pprint(len(data[3]['data']))


def test_timestamp():
    """"
    查询系统当前时间
    :return: {'data': 1536208800588, 'status': 'ok'}
    """
    data = huobi_timestamp()
    pprint(data)


def test_account():
    """
    查询当前用户的所有账户(即account-id)，Pro站和HADAX account-id通用
    :return: is_ok:True/False
            status_code:200
            response:
            result: {'data': None,
                  'err-code': 'api-signature-not-valid',
                  'err-msg': 'Signature not valid: Verification failure [校验失败]',
                  'status': 'error'}

                   {'data': [{'id': 4756379,
                              'state': 'working', working：正常, lock：账户被锁定
                              'subtype': '',
                              'type': 'spot'},  spot：现货账户， margin：杠杆账户，
                                                otc：OTC账户，point：点卡账户
                            {'id': 4817995, 'state': 'working',
                                'subtype': '', 'type': 'otc'}],
                  'status': 'ok'}
    """
    data = huobi_account()
    pprint(data)


def test_account_balance():
    """
    默认 查询Pro站指定账户的余额
    查询HADAX站指定账户的余额

    account-id	true	string	账户ID，可用 GET /v1/account/accounts 获取
    site	false	string	查询站	hadax

    :return:
            {'data': {'id': 4756379,
                   'list': [{'balance': '0', 余额
                             'currency': 'hb10', 币种
                             'type': 'trade'},], 类型  trade: 交易余额，frozen: 冻结余额
                   'state': 'working',
                   'type': 'spot'},
          'status': 'ok'}
    """
    data = huobi_account_balance('4756379')
    pprint(data)


def test_orders_place():
    """
    默认 Pro站下单
    HADAX站下单

    account-id	true string	账户 ID，币币交易使用‘spot’账户的accountid；
                                        借贷资产交易，请使用‘margin’账户的accountid
    amount	true	string	限价单表示下单数量，
                            市价买单时表示买多少钱，
                            市价卖单时表示卖多少币
                            最小数量0.001

    price	false	string	下单价格，市价单不传该参数
    source	false	string	订单来源	api，如果使用借贷资产交易，请填写‘margin-api’
    symbol	true	string	交易对		btcusdt, bchbtc, rcneth ...
    type	true	string	订单类型		buy-market：市价买, sell-market：市价卖,
                                        buy-limit：限价买, sell-limit：限价卖,
                                        buy-ioc：IOC买单, sell-ioc：IOC卖单,
                                        buy-limit-maker, sell-limit-maker(详细说明见下)

                            buy-limit-maker
                            当“下单价格”>=“市场最低卖出价”，订单提交后，系统将拒绝接受此订单；
                            当“下单价格”<“市场最低卖出价”，提交成功后，此订单将被系统接受。

                            sell-limit-maker
                            当“下单价格”<=“市场最高买入价”，订单提交后，系统将拒绝接受此订单；
                            当“下单价格”>“市场最高买入价”，提交成功后，此订单将被系统接受.

    :return: {'data': '11795183573', 'status': 'ok'})
    """
    data = huobi_orders_place('4756379', '0.0001', 'api', 'eoseth', 'buy-market',)
    pprint(data)
