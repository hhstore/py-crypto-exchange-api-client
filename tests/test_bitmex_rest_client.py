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
    """
    data = await bitmex_future_get_order(TEST_API_KEY, TEST_SECRET_KEY, 'XRPU18')
    pprint(data)
