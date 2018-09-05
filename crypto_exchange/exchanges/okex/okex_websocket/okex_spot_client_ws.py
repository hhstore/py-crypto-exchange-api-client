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
from pprint import pprint

from crypto_exchange.conf.exchange import Config
from crypto_exchange.exchanges.okex.okex_websocket.okex_spot_ws import OKexSpotWSClient

API_KEY = Config.exchange_api_key['okex']['public_key']
SECRET_KEY = Config.exchange_api_key['okex']['secret_key']


async def ws_spot_ticker(symbol):
    """
    订阅行情数据
    :param symbol:
    :return:
    """
    okex = OKexSpotWSClient(api_key=API_KEY, secret_key=SECRET_KEY)
    return await okex.ws_spot_ticker(symbol)


async def ws_spot_depth(symbol):
    """
    订阅币币市场深度(200增量数据返回)
    :param symbol:
    :return:
    """
    okex = OKexSpotWSClient(api_key=API_KEY, secret_key=SECRET_KEY)
    return await okex.ws_spot_depth(symbol)


async def ws_spot_depth_size(symbol, size):
    """
    订阅市场深度
    :param symbol:
    :param size:
    :return:
    """
    okex = OKexSpotWSClient(api_key=API_KEY, secret_key=SECRET_KEY)
    return await okex.ws_spot_depth_size(symbol, size)


async def ws_spot_deals(symbol):
    """
    订阅成交记录
    :param symbol:
    :return:
    """
    okex = OKexSpotWSClient(api_key=API_KEY, secret_key=SECRET_KEY)
    return await okex.ws_spot_deals(symbol)


async def ws_spot_k_line(symbol, k_line_type):
    """
    订阅K线数据
    :param symbol:
    :param k_line_type:
    :return:
    """
    okex = OKexSpotWSClient(api_key=API_KEY, secret_key=SECRET_KEY)
    return await okex.ws_spot_k_line(symbol, k_line_type)


async def ws_spot_login():
    """
    login 登录事件(个人信息推送)
    :return:
    """
    okex = OKexSpotWSClient(api_key=API_KEY, secret_key=SECRET_KEY)
    return await okex.ws_spot_login()


async def ws_spot_order(symbol):
    """
    交易数据
    :return:
    """
    okex = OKexSpotWSClient(api_key=API_KEY, secret_key=SECRET_KEY)
    return await okex.ws_spot_order(symbol)


async def ws_spot_balance(symbol):
    """
    账户信息
    :return:
    """
    okex = OKexSpotWSClient(api_key=API_KEY, secret_key=SECRET_KEY)
    return await okex.ws_spot_balance(symbol)
