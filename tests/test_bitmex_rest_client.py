from pprint import pprint

import pytest

from crypto_exchange.exchanges.bitmex.bitmax_rest.bitmex_rest_client import *

TEST_API_KEY = 'RGJtLQbuBq3wM-igto8XxmIV'
TEST_SECRET_KEY = 'SOZfYnTXsIIpGdSEhpZieLxtCWFfXbj0BYvRmPvI_otA-Wtt'
API_KEY = '3l5O7-JZxilRTrmF2Hz4t6cG'
SECRET_KEY = '3_h4n0B6NMvoxaXb8XcraDj4FmiImLF3h9xWkmOwdmXMiBCh'


@pytest.mark.asyncio
async def test_place_order():
    """
    下单

    :return: (True,
             200,
             <ClientResponse(https://testnet.bitmex.com/api/v1/order) [200 OK]>
            <CIMultiDictProxy('Date': 'Tue, 18 Sep 2018 10:04:38 GMT', 'Content-Type': 'application/json; charset=utf-8',
             'Transfer-Encoding': 'chunked', 'Connection': 'keep-alive',
              'Set-Cookie': '__cfduid=d747a1811a21896343945c7ebe492a77f1537265078; expires=Wed, 18-Sep-19 10:04:38 GMT;
              path=/; domain=.bitmex.com; HttpOnly; Secure',
              'X-RateLimit-Limit': '300', 'X-RateLimit-Remaining': '299', 'X-RateLimit-Reset': '1537265079',
              'X-Powered-By': 'Profit', 'Etag': 'W/"2b9-R426MoN1dADbubpy/DoX8PGIpe8"',
               'Strict-Transport-Security': 'max-age=31536000; includeSubDomains', 'Expect-CT': 'max-age=604800,
               report-uri="https://report-uri.cloudflare.com/cdn-cgi/beacon/expect-ct"', 'Server': 'cloudflare',
               'CF-RAY': '45c2fd54ee116da8-SJC', 'Content-Encoding': 'gzip')>
            ,
             {'account': 127045,
              'avgPx': None,
              'clOrdID': '',
              'clOrdLinkID': '',
              'contingencyType': '',
              'cumQty': 0,
              'currency': 'XBT',
              'displayQty': None,
              'exDestination': 'XBME',
              'execInst': '',
              'leavesQty': 1,
              'multiLegReportingType': 'SingleSecurity',
              'ordRejReason': '',
              'ordStatus': 'New',
              'ordType': 'Limit',
              'orderID': 'e593d8a1-07d8-ab36-ce94-6ff7b50f5d0b',
              'orderQty': 1,
              'pegOffsetValue': None,
              'pegPriceType': '',
              'price': 4e-05,
              'settlCurrency': 'XBt',
              'side': 'Buy',
              'simpleCumQty': 0,
              'simpleLeavesQty': 1,
              'simpleOrderQty': None,
              'stopPx': None,
              'symbol': 'XRPU18',
              'text': 'Submitted via API.',
              'timeInForce': 'GoodTillCancel',
              'timestamp': '2018-09-18T10:04:38.869Z',
              'transactTime': '2018-09-18T10:04:38.869Z',
              'triggered': '',
              'workingIndicator': True})

               {'error': {'message': 'This request has expired - `expires` is in the past. '
                                   'Current time: 1537266549',
                        'name': 'HTTPError'}}
    """
    data = await bitmex_future_place_order(TEST_API_KEY, TEST_SECRET_KEY, 'XRPU18', 'Buy', order_qty=1, price=0.00004,
                                           order_type='Limit')
    pprint(data)


@pytest.mark.asyncio
async def test_get_order():
    """
    查询订单
    :return:
     [{'account': 127045,
   'avgPx': None,
   'clOrdID': '',
   'clOrdLinkID': '',
   'contingencyType': '',
   'cumQty': 0,
   'currency': 'XBT',
   'displayQty': None,
   'exDestination': 'XBME',
   'execInst': '',
   'leavesQty': 0,
   'multiLegReportingType': 'SingleSecurity',
   'ordRejReason': '',
   'ordStatus': 'Canceled',
   'ordType': 'Limit',
   'orderID': '71b29380-70e4-c7be-0234-26785e0b3413',
   'orderQty': 1,
   'pegOffsetValue': None,
   'pegPriceType': '',
   'price': 4e-05,
   'settlCurrency': 'XBt',
   'side': 'Buy',
   'simpleCumQty': 0,
   'simpleLeavesQty': 0,
   'simpleOrderQty': None,
   'stopPx': None,
   'symbol': 'XRPU18',
   'text': 'Canceled: Canceled via API.\nSubmitted via API.',
   'timeInForce': 'GoodTillCancel',
   'timestamp': '2018-09-19T03:18:55.883Z',
   'transactTime': '2018-09-19T01:54:13.326Z',
   'triggered': '',
   'workingIndicator': False},
  {'account': 127045,
   'avgPx': None,
   'clOrdID': '',
   'clOrdLinkID': '',
   'contingencyType': '',
   'cumQty': 0,
   'currency': 'XBT',
   'displayQty': None,
   'exDestination': 'XBME',
   'execInst': '',
   'leavesQty': 1,
   'multiLegReportingType': 'SingleSecurity',
   'ordRejReason': '',
   'ordStatus': 'New',
   'ordType': 'Limit',
   'orderID': '5d22fbf6-223f-5bae-1010-a53e577608e4',
   'orderQty': 1,
   'pegOffsetValue': None,
   'pegPriceType': '',
   'price': 4e-05,
   'settlCurrency': 'XBt',
   'side': 'Buy',
   'simpleCumQty': 0,
   'simpleLeavesQty': 1,
   'simpleOrderQty': None,
   'stopPx': None,
   'symbol': 'XRPU18',
   'text': 'Submitted via API.',
   'timeInForce': 'GoodTillCancel',
   'timestamp': '2018-09-19T02:17:24.858Z',
   'transactTime': '2018-09-19T02:17:24.858Z',
   'triggered': '',
   'workingIndicator': True}]


     {'error': {'message': 'This request has expired - `expires` is in the past. '
                       'Current time: 1537327201',
            'name': 'HTTPError'}}
    """
    data = await bitmex_future_get_order(TEST_API_KEY, TEST_SECRET_KEY, 'XRPU18')
    pprint(data)


@pytest.mark.asyncio
async def test_delete_order():
    """
    撤销订单

    已撤销订单再次撤销返回相同数据

    :return:
    (True,
 200,
 <ClientResponse(https://testnet.bitmex.com/api/v1/order) [200 OK]>
<CIMultiDictProxy('Date': 'Wed, 19 Sep 2018 03:18:55 GMT', 'Content-Type': 'application/json; charset=utf-8', 'Transfer-Encoding': 'chunked', 'Connection': 'keep-alive', 'Set-Cookie': '__cfduid=deffc81bc1637f748130e0c709f51c88b1537327135; expires=Thu, 19-Sep-19 03:18:55 GMT; path=/; domain=.bitmex.com; HttpOnly; Secure', 'X-RateLimit-Limit': '300', 'X-RateLimit-Remaining': '299', 'X-RateLimit-Reset': '1537327136', 'X-Powered-By': 'Profit', 'Etag': 'W/"2de-/K7d03vpZKYTsoAnTqmKp7wLsBs"', 'Strict-Transport-Security': 'max-age=31536000; includeSubDomains', 'Expect-CT': 'max-age=604800, report-uri="https://report-uri.cloudflare.com/cdn-cgi/beacon/expect-ct"', 'Server': 'cloudflare', 'CF-RAY': '45c8e8626e806d3c-SJC', 'Content-Encoding': 'gzip')>
,
 [{'account': 127045,
   'avgPx': None,
   'clOrdID': '',
   'clOrdLinkID': '',
   'contingencyType': '',
   'cumQty': 0,
   'currency': 'XBT',
   'displayQty': None,
   'exDestination': 'XBME',
   'execInst': '',
   'leavesQty': 0,
   'multiLegReportingType': 'SingleSecurity',
   'ordRejReason': '',
   'ordStatus': 'Canceled',
   'ordType': 'Limit',
   'orderID': '71b29380-70e4-c7be-0234-26785e0b3413',
   'orderQty': 1,
   'pegOffsetValue': None,
   'pegPriceType': '',
   'price': 4e-05,
   'settlCurrency': 'XBt',
   'side': 'Buy',
   'simpleCumQty': 0,
   'simpleLeavesQty': 0,
   'simpleOrderQty': None,
   'stopPx': None,
   'symbol': 'XRPU18',
   'text': 'Canceled: Canceled via API.\nSubmitted via API.',
   'timeInForce': 'GoodTillCancel',
   'timestamp': '2018-09-19T03:18:55.883Z',
   'transactTime': '2018-09-19T01:54:13.326Z',
   'triggered': '',
   'workingIndicator': False}])


     {'error': {'message': 'This request has expired - `expires` is in the past. '
                       'Current time: 1537327322',
            'name': 'HTTPError'}}
    """
    data = await bitmex_future_delete_order(TEST_API_KEY, TEST_SECRET_KEY, '71b29380-70e4-c7be-0234-26785e0b3413')
    pprint(data)
