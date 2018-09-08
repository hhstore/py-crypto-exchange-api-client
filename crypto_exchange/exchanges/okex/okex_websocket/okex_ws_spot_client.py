# import websocket
# import time
# import sys
# import json
# import hashlib
# import zlib
# import base64
#
# api_key = ''
# secret_key = ""
#
#
#
#
# # spot trade
# def spotTrade(channel, api_key, secretkey, symbol, tradeType, price='', amount=''):
#     params = {
#         'api_key': api_key,
#         'symbol': symbol,
#         'type': tradeType
#     }
#     if price:
#         params['price'] = price
#     if amount:
#         params['amount'] = amount
#     sign = buildMySign(params, secretkey)
#     finalStr = "{'event':'addChannel','channel':'" + channel + "','parameters':{'api_key':'" + api_key + "',\
#                 'sign':'" + sign + "','symbol':'" + symbol + "','type':'" + tradeType + "'"
#     if price:
#         finalStr += ",'price':'" + price + "'"
#     if amount:
#         finalStr += ",'amount':'" + amount + "'"
#     finalStr += "},'binary':'true'}"
#     return finalStr
#
#
# # spot cancel order
# def spotCancelOrder(channel, api_key, secretkey, symbol, orderId):
#     params = {
#         'api_key': api_key,
#         'symbol': symbol,
#         'order_id': orderId
#     }
#     sign = buildMySign(params, secretkey)
#     return "{'event':'addChannel','channel':'" + channel + "','parameters':{'api_key':'" + api_key + "','sign':'" + sign + "','symbol':'" + symbol + "','order_id':'" + orderId + "'},'binary':'true'}"
#
#
# # subscribe trades for self
# def realtrades(channel, api_key, secretkey):
#     params = {'api_key': api_key}
#     sign = buildMySign(params, secretkey)
#     return "{'event':'addChannel','channel':'" + channel + "','parameters':{'api_key':'" + api_key + "','sign':'" + sign + "'},'binary':'true'}"
#
#
# # trade for future
# def futureTrade(api_key, secretkey, symbol, contractType, price='', amount='', tradeType='', matchPrice='',
#                 leverRate=''):
#     params = {
#         'api_key': api_key,
#         'symbol': symbol,
#         'contract_type': contractType,
#         'amount': amount,
#         'type': tradeType,
#         'match_price': matchPrice,
#         'lever_rate': leverRate
#     }
#     if price:
#         params['price'] = price
#     sign = buildMySign(params, secretkey)
#     finalStr = "{'event':'addChannel','channel':'ok_futuresusd_trade','parameters':{'api_key':'" + api_key + "',\
#                'sign':'" + sign + "','symbol':'" + symbol + "','contract_type':'" + contractType + "'"
#     if price:
#         finalStr += ",'price':'" + price + "'"
#     finalStr += ",'amount':'" + amount + "','type':'" + tradeType + "','match_price':'" + matchPrice + "','lever_rate':'" + leverRate + "'},'binary':'true'}"
#     return finalStr
#
#
# # future trade cancel
# def futureCancelOrder(api_key, secretkey, symbol, orderId, contractType):
#     params = {
#         'api_key': api_key,
#         'symbol': symbol,
#         'order_id': orderId,
#         'contract_type': contractType
#     }
#     sign = buildMySign(params, secretkey)
#     return "{'event':'addChannel','channel':'ok_futuresusd_cancel_order','parameters':{'api_key':'" + api_key + "',\
#             'sign':'" + sign + "','symbol':'" + symbol + "','contract_type':'" + contractType + "','order_id':'" + orderId + "'},'binary':'true'}"
#
#
# # subscribe future trades for self
# def futureRealTrades(api_key, secretkey):
#     params = {'api_key': api_key}
#     sign = buildMySign(params, secretkey)
#     return "{'event':'addChannel','channel':'ok_sub_futureusd_trades','parameters':{'api_key':'" + api_key + "','sign':'" + sign + "'},'binary':'true'}"
#
#
# def on_open(self):
#     # subscribe okcoin.com spot ticker
#     self.send("{'event':'addChannel','channel':'ok_sub_spotusd_btc_ticker','binary':'true'}")
#
#     # subscribe okcoin.com future this_week ticker
#     # self.send("{'event':'addChannel','channel':'ok_sub_futureusd_btc_ticker_this_week','binary':'true'}")
#
#     # subscribe okcoin.com future depth
#     # self.send("{'event':'addChannel','channel':'ok_sub_futureusd_ltc_depth_next_week_20','binary':'true'}")
#
#     # subscrib real trades for self
#     # realtradesMsg = realtrades('ok_sub_spotusd_trades',api_key,secret_key)
#     # self.send(realtradesMsg)
#
#     # spot trade via websocket
#     # spotTradeMsg = spotTrade('ok_spotusd_trade',api_key,secret_key,'ltc_usd','buy_market','1','')
#     # self.send(spotTradeMsg)
#
#     # spot trade cancel
#     # spotCancelOrderMsg = spotCancelOrder('ok_spotusd_cancel_order',api_key,secret_key,'btc_usd','125433027')
#     # self.send(spotCancelOrderMsg)
#
#     # future trade
#     # futureTradeMsg = futureTrade(api_key,secret_key,'btc_usd','this_week','','2','1','1','20')
#     # self.send(futureTradeMsg)
#
#     # future trade cancel
#     # futureCancelOrderMsg = futureCancelOrder(api_key,secret_key,'btc_usd','65464','this_week')
#     # self.send(futureCancelOrderMsg)
#
#     # subscrbe future trades for self
#     # futureRealTradesMsg = futureRealTrades(api_key,secret_key)
#     # self.send(futureRealTradesMsg)
#
#
# def on_message(self, evt):
#     data = inflate(evt)  # data decompress
#     print(data)
#
#
# def inflate(data):
#     decompress = zlib.decompressobj(
#         -zlib.MAX_WBITS  # see above
#     )
#     inflated = decompress.decompress(data)
#     inflated += decompress.flush()
#     return inflated
#
#
# def on_error(self, evt):
#     print(evt)
#
#
# def on_close(self, evt):
#     print('DISCONNECT')
#
#
# if __name__ == "__main__":
#     websocket.enableTrace(False)
#     if len(sys.argv) < 2:
#         host = url
#     else:
#         host = sys.argv[1]
#     ws = websocket.WebSocketApp(host,
#                                 on_message=on_message,
#                                 on_error=on_error,
#                                 on_close=on_close)
#     ws.on_open = on_open
#     ws.run_forever()

import logging

from pprint import pprint

from crypto_exchange.exchanges.okex.okex_websocket.okex_ws import OKEx

logger = logging.getLogger(__name__)
API_KEY = "3b773537-bbae-4db9-9a9b-42069d7e1fbb"
SECRET_KEY = "EFAABB4F616059E45557329A86D2B77C"


def okex_spot_ticker(symbol: str):
    """
    订阅行情数据
    :param symbol
    :return:
    """
    okex_spot = OKEx()
    okex_spot.send_sub("{'event':'addChannel','channel':'ok_sub_spot_%s_ticker'}" % symbol)

    yield from okex_spot.recv()


def okex_spot_depth(symbol: str):
    """
    订阅币币市场深度(200增量数据返回)
    第一次返回全量数据，根据接下来数据对第一次返回数据进行如下操作：删除（量为0时）；修改（价格相同量不同）；增加（价格不存在）
    :param symbol:
    :return:
    """
    okex_spot = OKEx()
    okex_spot.send_sub("{'event':'addChannel','channel':'ok_sub_spot_%s_depth'}" % symbol)

    yield from okex_spot.recv()


def okex_spot_depth_size(symbol: str, size: str):
    """
    订阅市场深度
    :param symbol:值为币对，如ltc_btc
    :param size值为获取深度条数，如5，10，20
    :return:
    """
    okex_spot = OKEx()
    okex_spot.send_sub("{'event':'addChannel','channel':'ok_sub_spot_%s_depth_%s'}" % (symbol, size))

    yield from okex_spot.recv()


def okex_spot_deals(symbol: str):
    """
    订阅成交记录
    :param symbol:值为币对，如ltc_btc
    :return:
    """
    okex_spot = OKEx()
    okex_spot.send_sub("{'event':'addChannel','channel':'ok_sub_spot_%s_deals'}" % symbol)

    yield from okex_spot.recv()


def okex_spot_k_line_size(symbol: str, size: str):
    """
     订阅K线数据
    :param symbol:值为币对，如ltc_btc
    :param size:值为K线时间周期，如1min, 3min, 5min, 15min, 30min, 1hour, 2hour, 4hour, 6hour, 12hour, day, 3day, week
    :return:
    """
    okex_spot = OKEx()
    okex_spot.send_sub("{'event':'addChannel','channel':'ok_sub_spot_%s_kline_%s'}" % (symbol, size))

    yield from okex_spot.recv()


def okex_spot_login():
    """
    # TODO 文档描述不清晰
    login 登录事件(个人信息推送)
    api_key	用户申请的APIKEY
    sign	请求参数的签名
    :return:
    """

    params = {}
    api_key = API_KEY
    secret_key = SECRET_KEY

    okex_spot = OKEx()
    sign = okex_spot.sign(params, secret_key)
    okex_spot.send_sub("""{"event":"login","parameters":{"api_key":%s,"sign":%s}}""" % (api_key, sign))

    yield from okex_spot.recv()


# 订阅行情数据
# data = okex_spot_ticker('bch_btc')

# 订阅币币市场深度(200增量数据返回)
# data = okex_spot_depth('bch_btc')

# 订阅市场深度
# data = okex_spot_depth_size('bch_btc', '10')

# 订阅成交记录
data = okex_spot_deals('bch_btc')

# login 登录事件(个人信息推送)
# data = okex_spot_login()
for i in data:
    pprint(i)
