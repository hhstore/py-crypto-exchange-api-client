import logging
import re
import time

from crypto_exchange.exchanges.huobi.huobi_rest.huobi_spot_client import huobi_spot_place_order
from crypto_exchange.exchanges.okex.okex_rest.okex_future_client import okex_future_place_order
from crypto_exchange.exchanges.okex.okex_rest.okex_spot_client import okex_spot_place_order

logger = logging.getLogger(__name__)
FUTURE_TYPE = ('this_week', 'next_week', 'quarter')
HUOBI_SPOT_TRADE_TYPE = ('buy-market', 'sell-market', 'buy-limit', 'sell-limit',
                         'buy-ioc', 'sell-ioc', 'buy-limit-marker', 'sell-limit-marker')
OKEX_SPOT_TRADE_TYPE = ('buy', 'sell', 'buy_market', 'sell_market')


OrderSide.BUY_MARKET

class OrderSide:
    BUY_MARKET = 0


async def place_order(exchange_name: str, public_key: str, secret_key: str, product_type: str, coin_type: str,
                      spot_trade_type: str = None, future_type: str = None, future_trade_type: str = None,
                      match_price: str = '0',
                      lever_rate: str = '10', price: str = '0',
                      volume: str = '0',
                      source='api'):
    """
    下单
    :param exchange_name: 交易所名称
    :param public_key:
    :param secret_key:
    :param product_type: 现货(spot) 期货(futures)
    :param coin_type: 交易对
    :param spot_trade_type: 现货类型
    :param future_type: 期货类型
    :param future_trade_type: 期货交易类型
    :param match_price: 是否为对手价
    :param lever_rate: 杠杆倍数
    :param price:
    :param volume:
    :param source: 订单来源
    :return:
    """
    # data = ''
    # model_str = 'from crypto_exchange.exchanges.{0}.{0}_rest.{0}_{1}_client '
    # 'import {0}_{1}_place_order as p_order'.format(
    #     exchange_name, product_type)
    # exec(model_str)
    # print(model_str)
    # time.sleep(10)
    # if product_type == 'spot':
    #     data = p_order(public_key, secret_key, coin_type, spot_type, amount, price, source=source)
    # return data
    data = ''

    # 火币 现货交易
    if exchange_name == 'huobi' and product_type == 'spot':
        data = await huobi_spot_place_order(public_key, secret_key, coin_type, spot_trade_type, volume, price,
                                            source=source)
        # 错误
        if re.search('err-code', str(data[-1])):
            data = {'status': data[-1]['status'], 'error_code': data[-1]['err-code'], 'err-msg': data[-1]['err-msg']}
            return data
        # 正常
        data = {'status': 'ok', 'status_code': data[1], 'order_id': data[-1]['data']}

    # okex 现货交易
    elif exchange_name == 'okex' and product_type == 'spot':
        data = await okex_spot_place_order(public_key, secret_key, coin_type, spot_trade_type, price, volume)
        # 错误
        if re.search('error_code', str(data[-1])):
            data = {'status': 'error', 'error_code': data[-1]['error_code'], }
            return data
        # 正常
        data = {'status': 'ok', 'status_code': data[1], 'order_id': data[-1]['order_id'], }

    # okex 期货交易
    elif exchange_name == 'okex' and product_type == 'future':
        data = await okex_future_place_order(public_key, secret_key, coin_type, future_type, price, volume,
                                             future_trade_type,
                                             match_price, lever_rate)
        # 错误
        if re.search('error_code', str(data[-1])):
            data = {'status': 'error', 'error_code': data[-1]['error_code'], 'error_msg': ''}
            return data
        # 正常
        data = {'status': 'ok', 'status_code': data[1], 'order_id': data[-1]['order_id'], }

    return data


async def cancel_order():
    pass
