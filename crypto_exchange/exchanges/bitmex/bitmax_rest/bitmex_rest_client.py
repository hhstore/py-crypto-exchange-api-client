# Testbitmex
from pprint import pprint

from crypto_exchange.exchanges.bitmex.bitmax_rest.bitmex_rest import BitMexFuture
TEST_URL = 'https://testnet.bitmex.com/api'
TEST_API_KEY = 'RGJtLQbuBq3wM-igto8XxmIV'
TEST_SECRET_KEY = 'SOZfYnTXsIIpGdSEhpZieLxtCWFfXbj0BYvRmPvI_otA-Wtt'
API_KEY = '3l5O7-JZxilRTrmF2Hz4t6cG'
SECRET_KEY = '3_h4n0B6NMvoxaXb8XcraDj4FmiImLF3h9xWkmOwdmXMiBCh'


async def bitmex_future_place_order():
    bitmex = BitMexFuture(TEST_API_KEY,TEST_SECRET_KEY,TEST_URL)
    return await bitmex.place_order('XRPU18','Buy',order_qty=1,price=0.00004,order_type='Limit')
