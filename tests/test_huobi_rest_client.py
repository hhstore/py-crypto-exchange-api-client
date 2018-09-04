from pprint import pprint

import logging

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
    """
    data = huobi_account()
    pprint(data)
