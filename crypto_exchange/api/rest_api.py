import logging
import re
import time

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


async def place_order(exchange_name: str, public_key: str, secret_key: str, product_type: str, coin_type: str,
                      order_side: str, spot_order_type: str = None, future_type: str = None,
                      future_trade_type: str = None,
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
    :param order_side: ask bid
    :param spot_order_type: limit market ioc
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

    spot_trade_type = ORDERSIDE.get('{}_{}_{}'.format(exchange_name, order_side, spot_order_type), None)

    # if product_type == 'spot':
    #     fun = PLACE_ORDER.get('{}_{}_place_order'.format(exchange_name, product_type), function)
    #     data = await fun(public_key,secret_key,coin_type,spot_trade_type,volume, price,source=source)
    #     # 错误
    #     if re.search('err-code', str(data[-1])):
    #         data = {'status': data[-1]['status'], 'error_code': data[-1]['err-code'], 'err-msg': data[-1]['err-msg']}
    #         return data
    #         # 正常
    #     data = {'status': 'ok', 'status_code': data[1], 'order_id': data[-1]['data']}

    # 火币 现货交易
    if exchange_name == 'huobi' and product_type == 'spot':
        data = await huobi_spot_place_order(public_key, secret_key, coin_type, spot_trade_type, volume, price,
                                            source=source)
        # 错误
        if re.search('err-code', str(data[-1])):
            data = {'status': data[-1]['status'], 'error_code': data[-1]['err-code'], 'err_msg': data[-1]['err-msg']}
            return data
        # 正常
        if re.search('data', str(data[-1])):
            data = {'status': 'ok', 'status_code': data[1], 'order_id': data[-1]['data']}
        return data

    # okex 现货交易
    elif exchange_name == 'okex' and product_type == 'spot':
        data = await okex_spot_place_order(public_key, secret_key, coin_type, spot_trade_type, volume, price)
        # 错误
        if re.search('error_code', str(data[-1])):
            error_code = data[-1]['error_code']
            data = {'status': 'error', 'error_code': error_code,
                    'err_msg': ERROR_CODE.get(str(error_code), '')}
            return data
        # 正常
        if re.search('order_id', str(data[-1])):
            data = {'status': 'ok', 'status_code': data[1], 'order_id': data[-1]['order_id'], }
        return data

    # okex 期货交易
    elif exchange_name == 'okex' and product_type == 'future':
        data = await okex_future_place_order(public_key, secret_key, coin_type, future_type, price, volume,
                                             future_trade_type,
                                             match_price, lever_rate)
        # 错误
        if re.search('error_code', str(data[-1])):
            error_code = data[-1]['error_code']
            data = {'status': 'error', 'error_code': error_code,
                    'error_msg': ERROR_CODE.get(str(error_code), '')}
            return data
        # 正常
        if re.search('order_id', str(data[-1])):
            data = {'status': 'ok', 'status_code': data[1], 'order_id': data[-1]['order_id'], }

        return data


CANCEL_ORDER = {
    'okex_spot_cancel_order': okex_spot_cancel_order,
    'okex_future_cancel_order': okex_future_cancel_order,
    'huobi_spot_cancel_order': huobi_spot_cancel_order,
}


async def cancel_order(exchange_name: str, public_key: str, secret_key: str, product_type: str,
                       order_id: str, coin_type: str = None, future_type: str = None):
    """
    撤销订单
    :param exchange_name: 交易所
    :param public_key:
    :param secret_key:
    :param product_type:
    :param coin_type: 交易对
    :param order_id: 订单号
    :param future_type: 期货类型
    :return:
    """
    if product_type == 'spot' and exchange_name == 'okex':
        fun = CANCEL_ORDER.get('{}_{}_cancel_order'.format(exchange_name, product_type), None)
        data = await fun(public_key, secret_key, order_id, coin_type, )
        # 错误
        if re.search('error_code', str(data[-1])):
            error_code = data[-1]['error_code']
            data = {'status': 'error', 'error_code': error_code,
                    'err_msg': ERROR_CODE.get(str(error_code), '')}
            return data
        # 正常
        if re.search('order_id', str(data[-1])):
            data = {'status': 'ok', 'status_code': data[1], 'order_id': data[-1]['order_id'],
                    'result': data[-1]['result']}
        return data

    elif product_type == 'spot' and exchange_name == 'huobi':
        fun = CANCEL_ORDER.get('{}_{}_cancel_order'.format(exchange_name, product_type), None)
        data = await fun(public_key, secret_key, order_id, )
        # 错误
        if re.search('err-code', str(data[-1])):
            data = {'status': data[-1]['status'], 'error_code': data[-1]['err-code'], 'err_msg': data[-1]['err-msg']}
            return data
        # 正常
        if re.search('data', str(data[-1])):
            data = {'status': data[-1]['status'], 'status_code': data[1], 'order_id': data[-1]['data'],
                    'result': 'True'}
        return data

    elif product_type == 'future' and exchange_name == 'okex':
        fun = CANCEL_ORDER.get('{}_{}_cancel_order'.format(exchange_name, product_type), None)
        data = await fun(public_key, secret_key, future_type, order_id, coin_type)
        # 错误
        if re.search('error_code', str(data[-1])):
            error_code = data[-1]['error_code']
            data = {'status': 'error', 'error_code': error_code,
                    'err_msg': ERROR_CODE.get(str(error_code), '')}
            return data
        # 正常
        if re.search('order_id', str(data[-1])):
            data = {'status': 'ok', 'status_code': data[1], 'order_id': data[-1]['order_id'],
                    'result': data[-1]['result']}
        return data


ORDER_INFO = {
    'okex_spot_order_info': okex_spot_order_info,
    'okex_future_order_info': okex_future_order_info,
    'huobi_spot_order_info': huobi_spot_order_info,
}


async def order_info(exchange_name: str, public_key: str, secret_key: str, product_type: str, order_id: str,
                     coin_type: str = None,
                     status: str = None, future_type: str = None):
    """
    订单详情
    :param exchange_name:
    :param public_key:
    :param secret_key:
    :param product_type:
    :param order_id:
    :param coin_type:
    :param future_type:
    :param status:
    :return:
    """
    if exchange_name == 'okex' and product_type == 'spot':
        fun = ORDER_INFO.get('{}_{}_order_info'.format(exchange_name, product_type))
        data = await fun(public_key, secret_key, coin_type, order_id)
        # 错误
        if re.search('error_code', str(data[-1])):
            # TODO
            error_code = data[-1]['error_code']
            data = {'status': 'error', 'error_code': error_code,
                    'err_msg': ERROR_CODE.get(str(error_code), '')}
            return data
    elif exchange_name == 'okex' and product_type == 'future':
        fun = ORDER_INFO.get('{}_{}_order_info'.format(exchange_name, product_type))
        data = await fun(public_key, secret_key, coin_type, future_type, order_id, status)

    elif exchange_name == 'huobi' and product_type == 'spot':
        fun = ORDER_INFO.get('{}_{}_order_info'.format(exchange_name, product_type))
        data = await fun(public_key, secret_key, order_id)

        # 错误
        if re.search('err-code', str(data[-1])):
            # TODO
            error_code = data[-1]['error_code']
            data = {'status': 'error', 'error_code': error_code,
                    'err_msg': ERROR_CODE.get(str(error_code), '')}
            return data

        # 正确
        if re.search('id', str(data[-1])):
            data = {
                'order_id': data[-1]['data']['id'], 'volume': data[-1]['data']['amount'],
                'price': data[-1]['data']['price'], 'create_date': data[-1]['data']['created-at'],
                'order_status': data[-1]['data']['state'], 'coin_type': data[-1]['data']['symbol'],
                'trade_type': data[-1]['data']['type']
            }
        return data

    else:
        return
