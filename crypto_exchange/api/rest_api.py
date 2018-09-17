import logging
import re
import time
from pprint import pprint

from crypto_exchange.exchanges.huobi.huobi_rest.huobi_spot_client import *
from crypto_exchange.exchanges.okex.okex_rest.okex_future_client import *
from crypto_exchange.exchanges.okex.okex_rest.okex_spot_client import *

logger = logging.getLogger(__name__)
FUTURE_TYPE = ('this_week', 'next_week', 'quarter')

ORDERSIDE = {
    'okex_bid_limit': 'buy',
    'okex_ask_limit': 'sell',
    'okex_bid_market': 'buy_market',
    'okex_ask_market': 'sell_market',
    'huobi_bid_limit': 'buy-limit',
    'huobi_ask_limit': 'shell-limit',
    'huobi_bid_market': 'buy-market',
    'huobi_ask_market': 'sell-market',
    'huobi_bid_ioc': 'buy-ioc',
    'huobi_ask_ioc': 'sell-ioc',
}

PLACE_ORDER = {
    'huobi_spot_place_order': huobi_spot_place_order,
    'okex_spot_place_order': okex_spot_place_order,
    'okex_future_place_order': okex_future_place_order,
}

ERROR_CODE = {
    '10000': '必选参数不能为空',
    '10001': '用户请求频率过快，超过该接口允许的限额',
    '10002': '系统错误',
    '10004': '请求失败',
    '10005': 'SecretKey不存在',
    '10006': 'Api_key不存在',
    '10007': '签名不匹配',
    '10008': '非法参数',
    '10009': '订单不存在',
    '10010': '余额不足',
    '10011': '买卖的数量小于BTC/LTC最小买卖额度',
    '10012': '当前网站暂时只支持btc_usd ltc_usd',
    '10013': '此接口只支持https请求',
    '10014': '下单价格不得≤0或≥',
    '10015': '下单价格与最新成交价偏差过大',
    '10016': '币数量不足',
    '10017': 'API鉴权失败',
    '10018': '借入不能小于最低限额[USD:100,BTC:0.1,LTC:1]',
    '10019': '页面没有同意借贷协议',
    '10020': '费率不能大于1%',
    '10021': '费率不能小于0.01%',
    '10023': '获取最新成交价错误',
    '10024': '可借金额不足',
    '10025': '额度已满，暂时无法借款',
    '10026': '借款(含预约借款)及保证金部分不能提出',
    '10027': '修改敏感提币验证信息，24小时内不允许提现',
    '10028': '提币金额已超过今日提币限额',
    '10029': '账户有借款，请撤消借款或者还清借款后提币',
    '10031': '存在BTC/LTC充值，该部分等值金额需6个网络确认后方能提出',
    '10032': '未绑定手机或谷歌验证',
    '10033': '服务费大于最大网络手续费',
    '10034': '服务费小于最低网络手续费',
    '10035': '可用BTC/LTC不足',
    '10036': '提币数量小于最小提币数量',
    '10037': '交易密码未设置',
    '10040': '取消提币失败',
    '10041': '提币地址不存在或未认证',
    '10042': '交易密码错误',
    '10043': '合约权益错误，提币失败',
    '10044': '取消借款失败',
    '10047': '当前为子账户，此功能未开放',
    '10048': '提币信息不存在',
    '10049': '小额委托(<0.15BTC)的未成交委托数量不得大于50个',
    '10050': '重复撤单',
    '10052': '提币受限',
    '10056': '划转受限',
    '10057': '划转失败',
    '10058': 'NEO只能提整数',
    '10064': '美元充值后的48小时内，该部分资产不能提出',
    '10100': '账户被冻结',
    '10101': '订单类型错误',
    '10102': '不是本用户的订单',
    '10103': '私密订单密钥错误',
    '10106': 'apiKey所属域名不匹配',
    '10216': '非开放API',
    '1002': '交易金额大于余额',
    '1003': '交易金额小于最小交易值',
    '1004': '交易金额小于0',
    '1007': '没有交易市场信息',
    '1008': '没有最新行情信息',
    '1009': '没有订单',
    '1010': '撤销订单与原订单用户不一致',
    '1011': '没有查询到该用户',
    '1013': '没有订单类型',
    '1014': '没有登录',
    '1015': '没有获取到行情深度信息',
    '1017': '日期参数错误',
    '1018': '下单失败',
    '1019': '撤销订单失败',
    '1024': '币种不存在',
    '1025': '没有K线类型',
    '1026': '没有基准币数量',
    '1027': '参数不合法可能超出限制',
    '1028': '保留小数位失败',
    '1029': '正在准备中',
    '1030': '有融资融币无法进行交易',
    '1031': '转账余额不足',
    '1032': '该币种不能转账',
    '1035': '密码不合法',
    '1036': '谷歌验证码不合法',
    '1037': '谷歌验证码不正确',
    '1038': '谷歌验证码重复使用',
    '1039': '短信验证码输错限制',
    '1040': '短信验证码不合法',
    '1041': '短信验证码不正确',
    '1042': '谷歌验证码输错限制',
    '1043': '登陆密码不允许与交易密码一致',
    '1044': '原密码错误',
    '1045': '未设置二次验证',
    '1046': '原密码未输入',
    '1048': '用户被冻结',
    '1050': '订单已撤销或者撤单中',
    '1051': '订单已完成交易',
    '1056': '划转受限',
    '1057': '划转失败',
    '1058': 'NEO只能提整数',
    '1201': '账号零时删除',
    '1202': '账号不存在',
    '1203': '转账金额大于余额',
    '1204': '不同种币种不能转账',
    '1205': '账号不存在主从关系',
    '1206': '提现用户被冻结',
    '1207': '不支持转账',
    '1208': '没有该转账用户',
    '1209': '当前api不可用',
    '1216': '市价交易暂停，请选择限价交易',
    '1217': '您的委托价格超过最新成交价的±5%，存在风险，请重新下单',
    '1218': '下单失败，请稍后再试',
    '20001': '用户不存在',
    '20002': '用户被冻结',
    '20003': '用户被爆仓冻结',
    '20004': '合约账户被冻结',
    '20005': '用户合约账户不存在',
    '20006': '必填参数为空',
    '20007': '参数错误',
    '20008': '合约账户余额为空',
    '20009': '虚拟合约状态错误',
    '20010': '合约风险率信息不存在',
    '20011': '10倍/20倍杠杆开BTC前保证金率低于90%/80%，10倍/20倍杠杆开LTC前保证金率低于80%/60%',
    '20012': '10倍/20倍杠杆开BTC后保证金率低于90%/80%，10倍/20倍杠杆开LTC后保证金率低于80%/60%',
    '20013': '暂无对手价',
    '20014': '系统错误',
    '20015': '订单信息不存在',
    '20016': '平仓数量是否大于同方向可用持仓数量',
    '20017': '非本人操作',
    '20018': '下单价格高于前一分钟的103%或低于97%',
    '20019': '该IP限制不能请求该资源',
    '20020': '密钥不存在',
    '20021': '指数信息不存在',
    '20022': '接口调用错误（全仓模式调用全仓接口，逐仓模式调用逐仓接口）',
    '20023': '逐仓用户',
    '20024': 'sign签名不匹配',
    '20025': '杠杆比率错误',
    '20026': 'API鉴权错误',
    '20027': '无交易记录',
    '20028': '合约不存在',
    '20029': '转出金额大于可转金额',
    '20030': '账户存在借款',
    '20038': '根据相关法律，您所在的国家或地区不能使用该功能。',
    '20049': '用户请求接口过于频繁',
    '20061': '合约相同方向只支持一个杠杆，若有10倍多单，就不能再下20倍多单',
    '21005': '请求接口失败，请您重试',
    '21020': '合约交割中，无法下单',
    '21021': '合约清算中，无法下单',
    '21023': '当前全仓方向仓位已超过最大可开张数',
    '21024': '当前逐仓方向仓位已超过最大可开张数',
    '21025': '下单后保证金率小于对应档位要求的最低保证金率',
    '21026': '您的账户已被限制开仓操作',
    'HTTP错误码403 ': '用户请求过快，IP被屏蔽',
    'Ping不通 ': '用户请求过快，IP被屏蔽'
}
OKEX_FUTURE_AMOUNT_LIMIT = 0.0001
OKEX_AMOUNT_LIMIT = {
    'btc_usdt': 0.00000001,
    'ltc_usdt': 0.000001,
    'eth_usdt': 0.000001,
    'okb_usdt': 0.0001,
    'etc_usdt': 0.00001,
    'bch_usdt': 0.00000001,
    'eos_usdt': 0.0001,
    'xmr_usdt': 0.000001,

    'ltc_btc': 0.000001,
    'eth_btc': 0.000001,
    'okb_btc': 0.0001,
    'etc_btc': 0.00001,
    'bch_btc': 0.00000001,
    'eos_btc': 0.0001,
    'xmr_btc': 0.000001,

    'ltc_eth': 0.001,
    'okb_eth': 0.0001,
    'etc_eth': 0.00001,
    'bch_eth': 0.00000001,
    'eos_eth': 0.0001,
    'xmr_eth': 0.000001,

    'ltc_okb': 0.000001,
    'etc_okb': 0.00001,
    'bch_okb': 0.000001,
    'eos_okb': 0.000001,
}

HUOBI_AMOUNT_LIMIT = {
    'btcusdt': 0.0001,
    'bchusdt': 0.0001,
    'ethusdt': 0.0001,
    'etcusdt': 0.0001,
    'ltcusdt': 0.0001,
    'eosusdt': 0.0001,

    'bchbtc': 0.0001,
    'ethetc': 0.0001,
    'ltcbtc': 0.0001,
    'etcbtc': 0.0001,
    'eosbtc': 0.01,
    'xmrbtc': 0.0001,

    'eoseth': 0.01,
    'xmreth': 0.0001,

    'eosht': 0.0001,
    'ltcht': 0.0001,
    'etcht': 0.0001,
    'bchht': 0.0001,
}


async def spot_place_order(exchange_name: str, public_key: str, secret_key: str, product_type: str, coin_type: str,
                           order_side: str, spot_order_type: str = None, price: str = '0', volume: str = '0',
                           source='api'):
    """
    现货下单交易
    :param exchange_name:
    :param public_key:
    :param secret_key:
    :param product_type:
    :param coin_type:
    :param order_side:
    :param spot_order_type:
    :param price:
    :param volume:
    :param source:
    :return:
    """
    spot_trade_type = ORDERSIDE.get('{}_{}_{}'.format(exchange_name, order_side, spot_order_type), None)

    # 火币 现货交易
    if exchange_name == 'huobi' and product_type == 'spot':
        fun = PLACE_ORDER.get('{}_{}_place_order'.format(exchange_name, product_type))
        is_ok, status_code, _, data = await fun(public_key, secret_key, coin_type, spot_trade_type, volume, price,
                                                source=source)
        result = {'status': is_ok}
        # 错误
        if re.search('err-code', str(data)):
            result = {
                'status': data.get('status'),
                'error_code': data.get('err-code'),
                'err_msg': data.get('err-msg'),
            }
            return result
        # 正常
        if re.search('data', str(data)):
            result = {
                'status': is_ok,
                'status_code': status_code,
                'order_id': data.get('data'),
            }
        return result

    # okex 现货交易
    elif exchange_name == 'okex' and product_type == 'spot':
        fun = PLACE_ORDER.get('{}_{}_place_order'.format(exchange_name, product_type))
        is_ok, status_code, _, data = await fun(public_key, secret_key, coin_type, spot_trade_type, volume, price)
        result = {'status': is_ok}
        # 错误
        if re.search('error_code', str(data)):
            error_code = data.get('error_code')
            result = {
                'status': 'error',
                'error_code': error_code,
                'err_msg': ERROR_CODE.get(str(error_code), '')
            }
            return result
        # 正常
        if re.search('order_id', str(data)):
            result = {
                'status': is_ok,
                'status_code': status_code,
                'order_id': data.get('order_id'),
            }
        return result
    else:
        return


async def future_place_order(exchange_name: str, public_key: str, secret_key: str, product_type: str, coin_type: str,
                             order_side: str, future_type: str = None,
                             future_trade_type: str = None,
                             match_price: str = '0',
                             lever_rate: str = '10', price: str = '0',
                             volume: str = '0', ):
    """
    期货下单交易
    :param exchange_name:
    :param public_key:
    :param secret_key:
    :param product_type:
    :param coin_type:
    :param order_side:
    :param future_type:
    :param future_trade_type:
    :param match_price:
    :param lever_rate:
    :param price:
    :param volume:
    :return:
    """
    # okex 期货交易
    if exchange_name == 'okex' and product_type == 'future':
        fun = PLACE_ORDER.get('{}_{}_place_order'.format(exchange_name, product_type))
        is_ok, status_code, _, data = await fun(public_key, secret_key, coin_type, future_type, price, volume,
                                                future_trade_type,
                                                match_price, lever_rate)
        result = {'status': is_ok}
        # 错误
        if re.search('error_code', str(data)):
            error_code = data.get('error_code')
            result = {
                'status': 'error',
                'error_code': error_code,
                'error_msg': ERROR_CODE.get(str(error_code), '')
            }
            return result
        # 正常
        if re.search('order_id', str(data)):
            result = {
                'status': is_ok,
                'status_code': status_code,
                'order_id': data.get('order_id'),
            }

        return result
    else:
        return


PLACE_ORDERS = {
    'okex_spot_place_orders': okex_spot_batch_trade,
    'okex_future_place_orders': okex_future_batch_trade,
}


async def spot_place_orders(exchange_name: str, public_key: str, secret_key: str, product_type: str, coin_type: str,
                            orders_data: str, order_side: str = None, spot_order_type: str = None, ):
    """
    现货批量下单
    :param exchange_name:
    :param public_key:
    :param secret_key:
    :param product_type:
    :param coin_type:
    :param orders_data: String(格式[{price:3,amount:5,type:'sell'},{price:3,amount:3,type:'buy'}])
    :param order_side:
    :param spot_order_type:
    :return:
    """
    spot_trade_type = ORDERSIDE.get('{}_{}_{}'.format(exchange_name, order_side, spot_order_type), None)
    # okex 现货交易
    if exchange_name == 'okex' and product_type == 'spot':
        fun = PLACE_ORDERS.get('{}_{}_place_orders'.format(exchange_name, product_type))
        is_ok, status_code, _, data = await fun(public_key, secret_key, coin_type, orders_data, spot_trade_type)
        result = {'status': is_ok}
        # 错误
        if not re.search('order_id', str(data)):
            error_code = data.get('error_code')
            result = {
                'status': 'error',
                'error_code': error_code,
                'err_msg': ERROR_CODE.get(str(error_code), '')
            }
            return result
        # 正常
        if re.search('order_id', str(data)):
            orders_info = data.get('order_info')
            for order in orders_info:
                if order.get('errorCode'):
                    order['errorCode'] = ERROR_CODE.get(str(order['errorCode']), '')
            result = {
                'status': is_ok,
                'status_code': status_code,
                'order_info': orders_info,
            }
        return result
    else:
        return


async def future_place_orders(exchange_name: str, public_key: str, secret_key: str, product_type: str, coin_type: str,
                              future_type: str, orders_data: str, lever_rate: str = None):
    """
    期货批量下单
    :param exchange_name:
    :param public_key:
    :param secret_key:
    :param product_type:
    :param coin_type:
    :param future_type:
    :param orders_data:
    :param lever_rate:
    :return:
    """
    # okex 期货交易
    if exchange_name == 'okex' and product_type == 'future':
        fun = PLACE_ORDERS.get('{}_{}_place_orders'.format(exchange_name, product_type))
        is_ok, status_code, _, data = await fun(public_key, secret_key, coin_type, future_type, orders_data, lever_rate)

        result = {'status': is_ok}
        # 错误
        if not re.search('order_id', str(data)):
            error_code = data.get('error_code')
            result = {
                'status': 'error',
                'error_code': error_code,
                'error_msg': ERROR_CODE.get(str(error_code), '')
            }
            return result
        # 正常
        if re.search('order_id', str(data)):
            orders_info = data.get('order_info')
            for order in orders_info:
                if order.get('errorCode'):
                    order['errorCode'] = ERROR_CODE.get(str(order['errorCode']), '')
            result = {
                'status': is_ok,
                'status_code': status_code,
                'order_info': orders_info,
            }
        return result
    else:
        return


CANCEL_ORDER = {
    'okex_spot_cancel_order': okex_spot_cancel_order,
    'okex_future_cancel_order': okex_future_cancel_order,
    'huobi_spot_cancel_order': huobi_spot_cancel_order,
}


async def spot_cancel_order(exchange_name: str, public_key: str, secret_key: str, product_type: str,
                            order_id: str, coin_type: str = None, ):
    """
    现货撤销订单
    :param exchange_name:
    :param public_key:
    :param secret_key:
    :param product_type:
    :param order_id:
    :param coin_type:
    :return:
    """
    if product_type == 'spot' and exchange_name == 'okex':
        fun = CANCEL_ORDER.get('{}_{}_cancel_order'.format(exchange_name, product_type), None)
        is_ok, status_code, _, data = await fun(public_key, secret_key, order_id, coin_type, )
        result = {'status': is_ok}
        # 错误
        if re.search('error_code', str(data)):
            error_code = data.get('error_code')
            result = {
                'status': 'error',
                'error_code': error_code,
                'err_msg': ERROR_CODE.get(str(error_code), '')
            }
            return result
        # 正常
        if re.search('order_id', str(data)):
            result = {
                'status': is_ok,
                'status_code': status_code,
                'order_id': data.get('order_id'),
                'result': data.get('result'),
            }
        return result

    elif product_type == 'spot' and exchange_name == 'huobi':
        fun = CANCEL_ORDER.get('{}_{}_cancel_order'.format(exchange_name, product_type), None)
        is_ok, status_code, _, data = await fun(public_key, secret_key, order_id, )
        result = {'status': is_ok}
        # 错误
        if re.search('err-code', str(data)):
            result = {
                'status': data.get('status'),
                'error_code': data.get('err-code'),
                'err_msg': data.get('err-msg'),
            }
            return result
        # 正常
        if re.search('data', str(data)):
            result = {
                'status': data.get('status'),
                'status_code': status_code,
                'order_id': data.get('data'),
                'result': 'True'
            }
        return result
    else:
        return


async def future_cancel_order(exchange_name: str, public_key: str, secret_key: str, product_type: str,
                              order_id: str, coin_type: str = None, future_type: str = None):
    if product_type == 'future' and exchange_name == 'okex':
        fun = CANCEL_ORDER.get('{}_{}_cancel_order'.format(exchange_name, product_type), None)
        is_ok, status_code, _, data = await fun(public_key, secret_key, future_type, order_id, coin_type)
        result = {'status': is_ok}
        # 错误
        if re.search('error_code', str(data)):
            error_code = data.get('error_code')
            result = {
                'status': 'error',
                'error_code': error_code,
                'err_msg': ERROR_CODE.get(str(error_code), '')
            }
            return result
        # 正常
        if re.search('order_id', str(data)):
            result = {
                'status': 'ok',
                'status_code': status_code,
                'order_id': data.get('order_id'),
                'result': data.get('result'),
            }
        return result
    else:
        return


CANCEL_ORDERS = {
    'okex_spot_cancel_orders': okex_spot_cancel_order,
    'okex_future_cancel_orders': okex_future_cancel_order,
    'huobi_spot_cancel_orders': huobi_batch_cancel_orders(),
}

ORDER_INFO = {
    'okex_spot_order_info': okex_spot_order_info,
    'okex_future_order_info': okex_future_order_info,
    'huobi_spot_order_info': huobi_spot_order_info,
}


async def spot_order_info(exchange_name: str, public_key: str, secret_key: str, product_type: str, order_id: str,
                          coin_type: str,
                          status: str = None, ):
    """
    现货订单详情
    :param exchange_name:
    :param public_key:
    :param secret_key:
    :param product_type:
    :param order_id:
    :param coin_type:
    :param status:
    :return:
    """
    if exchange_name == 'okex' and product_type == 'spot':
        fun = ORDER_INFO.get('{}_{}_order_info'.format(exchange_name, product_type))
        is_ok, status_code, _, data = await fun(public_key, secret_key, coin_type, order_id)
        # pprint(data)
        result = {'status': is_ok}
        # 错误
        if re.search('error_code', str(data)):
            error_code = data.get('error_code')
            result = {
                'status': 'error',
                'error_code': error_code,
                'err_msg': ERROR_CODE.get(str(error_code), '')
            }
            return result
        elif re.search('order_id', str(data)):
            result = {
                'order_id': dict(data.get('orders')).get('order_id'),
                'volume': dict(data.get('orders')).get('amount'),
                'deal_volume': dict(data.get('orders')).get('deal_amount'),
                'price': dict(data.get('orders')).get('price'),
                'create_date': dict(data.get('orders')).get('create_date'),
                'order_status': dict(data.get('orders')).get('status'),
                'coin_type': dict(data.get('orders')).get('symbol'),
                'trade_type': dict(data.get('orders')).get('type'),
                'status': is_ok
            }
        return result

    elif exchange_name == 'huobi' and product_type == 'spot':
        fun = ORDER_INFO.get('{}_{}_order_info'.format(exchange_name, product_type))
        is_ok, status_code, _, data = await fun(public_key, secret_key, order_id)
        # pprint(data)
        result = {'status': is_ok}
        # 错误
        if re.search('err-code', str(data)):
            result = {
                'status': data.get('status'),
                'error_code': data.get('err-code'),
                'err_msg': data.get('err-msg'),
            }
            return result

        # 正确
        if re.search('id', str(data)):
            result = {
                'order_id': data.get('data').get('id'),
                'volume': data.get('data').get('amount'),
                'deal_volume': data.get('data').get('field-amount'),
                'price': data.get('data').get('price'),
                'create_date': data.get('data').get('created-at'),
                'order_status': data.get('data').get('state'),
                'coin_type': data.get('data').get('symbol'),
                'trade_type': data.get('data').get('type'),
                'status': is_ok,
            }
        return result

    else:
        return


async def future_order_info(exchange_name: str, public_key: str, secret_key: str, product_type: str, order_id: str,
                            future_type: str,
                            coin_type: str = None,
                            status: str = None, current_page: str = None,
                            page_length: str = None):
    """
    期货订单详情
    :param exchange_name:
    :param public_key:
    :param secret_key:
    :param product_type:
    :param order_id:
    :param coin_type:
    :param status:
    :param future_type:
    :param current_page:
    :param page_length:
    :return:
    """
    if exchange_name == 'okex' and product_type == 'future':
        fun = ORDER_INFO.get('{}_{}_order_info'.format(exchange_name, product_type))
        is_ok, status_code, _, data = await fun(public_key, secret_key, coin_type, future_type, order_id, status,
                                                current_page, page_length)
        pprint(data)
        result = {'status': is_ok}
        # 错误
        if re.search('error_code', str(data)):
            error_code = data.get('error_code')
            result = {
                'status': 'error',
                'error_code': error_code,
                'err_msg': ERROR_CODE.get(str(error_code), '')
            }
            return result

        # 正确
        if re.search('order_id', str(data)):
            # TODO 有可能返回多个值，列表里嵌套多个字典
            info = dict(data.get('orders')[0])
            result = {
                'order_id': info.get('order_id'),
                'volume': info.get('amount'),
                'deal_volume': info.get('deal_amount'),
                'price': info.get('price'),
                'create_date': info.get('create_date'),
                'order_status': info.get('status'),
                'coin_type': info.get('symbol'),
                'trade_type': info.get('type'),
                'status': is_ok,
            }
        return result
    else:
        return


async def spot_order_history():
    pass


DEPTH = {
    'okex_spot_depth': okex_spot_depth,
    'okex_future_depth': okex_future_depth,
    'huobi_spot_depth': huobi_spot_depth,
}


async def spot_depth(exchange_name: str, public_key: str, secret_key: str, product_type: str, coin_type: str,
                     depth_merge: str = 'step0',
                     depth_size: str = None):
    """
    现货市场深度
    :param exchange_name:
    :param public_key:
    :param secret_key:
    :param product_type:
    :param coin_type:
    :param depth_merge:
    :param depth_size:
    :return:
    """
    if exchange_name == 'okex' and product_type == 'spot':
        fun = DEPTH.get('{}_{}_depth'.format(exchange_name, product_type))
        is_ok, status_code, _, data = await fun(public_key, secret_key, coin_type, depth_size)
        pprint(data)
        result = {'status': is_ok}
        # 错误
        if re.search('error_code', str(data)):
            error_code = data.get('error_code')
            result = {
                'status': 'error',
                'error_code': error_code,
                'err_msg': ERROR_CODE.get(str(error_code), '')
            }
            return result
        elif re.search('asks', str(data)):
            result = {
                'asks': dict(data.get('asks')),
                'bids': dict(data.get('bids')),
                'status': is_ok
            }
        return result

    elif exchange_name == 'huobi' and product_type == 'spot':
        fun = DEPTH.get('{}_{}_depth'.format(exchange_name, product_type))
        is_ok, status_code, _, data = await fun(public_key, secret_key, coin_type, depth_merge)
        pprint(data)
        result = {'status': is_ok}
        # 错误
        if re.search('err-code', str(data)):
            result = {
                'status': data.get('status'),
                'error_code': data.get('err-code'),
                'err_msg': data.get('err-msg'),
            }
            return result

        # 正确
        if re.search('id', str(data)):
            result = {
                'asks': data.get('tick').get('asks'),
                'bids': data.get('tick').get('bids'),
                'status': is_ok,
            }
        return result

    else:
        return


async def future_depth(exchange_name: str, public_key: str, secret_key: str, product_type: str, coin_type: str,
                       future_type: str, depth_size: str,
                       depth_merge: int = 0, ):
    """
    期货市场深度
    :param exchange_name:
    :param public_key:
    :param secret_key:
    :param product_type:
    :param coin_type:
    :param future_type:
    :param depth_size:
    :param depth_merge:
    :return:
    """
    if exchange_name == 'okex' and product_type == 'future':
        fun = DEPTH.get('{}_{}_depth'.format(exchange_name, product_type))
        is_ok, status_code, _, data = await fun(public_key, secret_key, coin_type, future_type, depth_size, depth_merge)
        pprint(data)
        result = {'status': is_ok}
        # 错误
        if re.search('error_code', str(data)):
            error_code = data.get('error_code')
            result = {
                'status': 'error',
                'error_code': error_code,
                'err_msg': ERROR_CODE.get(str(error_code), '')
            }
            return result

        # 正确
        if re.search('asks', str(data)):
            result = {
                'asks': dict(data.get('asks')),
                'bids': dict(data.get('bids')),
                'status': is_ok,
            }
        return result
    else:
        return


WITHDRAW = {
    'okex_withdraw': okex_withdraw,
    'huobi_withdraw': huobi_withdraw,
}


async def withdraw(exchange_name: str, public_key: str, secret_key: str, coin_type: str, address: str, amount: str,
                   charge_fee: str, address_type: str, trade_password: str = None, address_tag: str = None):
    """
    提币
    :param exchange_name: 交易所
    :param public_key:
    :param secret_key:
    :param coin_type: 币种
    :param address: 提现地址
    :param amount: 提现数量
    :param charge_fee: 手续费
    :param address_type: 地址类型 okcn：国内站 okcom：国际站 okex：OKEX address：外部地址
    :param trade_password: 交易密码
    :param address_tag: 虚拟币共享地址tag
    :return:
    """
    if exchange_name == 'okex':
        fun = WITHDRAW.get(f'{exchange_name}_withdraw')
        is_ok, status_code, _, data = await fun(public_key, secret_key, coin_type, charge_fee, trade_password, address,
                                                amount, address_type)
        pprint(data)
        result = {'status': is_ok}
        # 错误
        if re.search('error_code', str(data)):
            error_code = data.get('error_code')
            result = {
                'status': 'error',
                'error_code': error_code,
                'err_msg': ERROR_CODE.get(str(error_code), '')
            }
            return result

        # 正确
        if re.search('withdraw_id', str(data)):
            result = {
                'withdraw_id': data.get('withdraw_id'),
                'status': is_ok,
            }
        return result

    elif exchange_name == 'huobi':
        fun = WITHDRAW.get(f'{exchange_name}_withdraw')
        is_ok, status_code, _, data = await fun(public_key, secret_key, coin_type, address, amount, charge_fee,
                                                address_tag)
        pprint(data)
        result = {'status': is_ok}
        # 错误
        if re.search('err-code', str(data)):
            result = {
                'status': data.get('status'),
                'error_code': data.get('err-code'),
                'err_msg': data.get('err-msg'),
            }
            return result

        # 正确
        if re.search('data', str(data)):
            result = {
                'withdraw_id': data.get('data'),
                'status': is_ok,
            }
        return result

    else:
        return


CANCEL_WITHDRAW = {
    'okex_cancel_withdraw': okex_cancel_withdraw,
    'huobi_cancel_withdraw': huobi_cancel_withdraw
}


async def cancel_withdraw(exchange_name: str, public_key: str, secret_key: str, coin_type: str, withdraw_id: str):
    """
    取消提币
    :param exchange_name: 交易所
    :param public_key:
    :param secret_key:
    :param coin_type: 币种
    :param withdraw_id: 提币ID
    :return:
    """
    if exchange_name == 'okex':
        fun = WITHDRAW.get(f'{exchange_name}_cancel_withdraw')
        is_ok, status_code, _, data = await fun(public_key, secret_key, coin_type, withdraw_id)
        pprint(data)
        result = {'status': is_ok}
        # 错误
        if re.search('error_code', str(data)):
            error_code = data.get('error_code')
            result = {
                'status': 'error',
                'error_code': error_code,
                'err_msg': ERROR_CODE.get(str(error_code), '')
            }
            return result

        # 正确
        if re.search('withdraw_id', str(data)):
            result = {
                'withdraw_id': data.get('withdraw_id'),
                'status': is_ok,
            }
        return result

    elif exchange_name == 'huobi':
        fun = WITHDRAW.get(f'{exchange_name}_withdraw')
        is_ok, status_code, _, data = await fun(public_key, secret_key, withdraw_id)
        pprint(data)
        result = {'status': is_ok}
        # 错误
        if re.search('err-code', str(data)):
            result = {
                'status': data.get('status'),
                'error_code': data.get('err-code'),
                'err_msg': data.get('err-msg'),
            }
            return result

        # 正确
        if re.search('data', str(data)):
            result = {
                'withdraw_id': data.get('data'),
                'status': is_ok,
            }
        return result

    else:
        return


BALANCE = {
    'okex_balance': okex_wallet_info,
    'huobi_balance': huobi_account_balance
}


async def balance(exchange_name: str, public_key: str, secret_key: str, ):
    """
    余额
    :param exchange_name:
    :param public_key:
    :param secret_key:
    :return:
    """
    if exchange_name == 'okex':
        fun = WITHDRAW.get(f'{exchange_name}_balance')
        is_ok, status_code, _, data = await fun(public_key, secret_key, )
        pprint(data)
        result = {'status': is_ok}
        # 错误
        if re.search('error_code', str(data)):
            error_code = data.get('error_code')
            result = {
                'status': 'error',
                'error_code': error_code,
                'err_msg': ERROR_CODE.get(str(error_code), '')
            }
            return result

        # 正确
        if re.search('free', str(data)):
            funds = data.get('funds')
            result = {
                'trade': funds.get('free'),
                'frozen': funds.get('holds'),
                'status': is_ok,
            }
        return result

    elif exchange_name == 'huobi':
        fun = WITHDRAW.get(f'{exchange_name}_balance')
        is_ok, status_code, _, data = await fun(public_key, secret_key, )
        pprint(data)
        result = {'status': is_ok}
        # 错误
        if re.search('err-code', str(data)):
            result = {
                'status': data.get('status'),
                'error_code': data.get('err-code'),
                'err_msg': data.get('err-msg'),
            }
            return result

        # 正确
        if re.search('balance', str(data)):
            if data.get('type') == 'spot':
                funds_list = data.get('list')
            trade_dict = {}
            frozen_dict = {}
            for item in funds_list:
                if item.get('type') == 'trade':
                    trade_dict[item.get('currency')] = item.get('balance')
                elif item.get('type') == 'frozen':
                    frozen_dict[item.get('currency')] = item.get('balance')
                else:
                    pass
            result = {
                'trade': trade_dict,
                'frozen': frozen_dict,
                'status': is_ok,
            }
        return result

    else:
        return
