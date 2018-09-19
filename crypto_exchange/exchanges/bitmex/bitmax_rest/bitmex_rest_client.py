# Testbitmex
import time
from pprint import pprint

from crypto_exchange.exchanges.bitmex.bitmax_rest.bitmex_rest import BitMexFuture

PARAMS_ERROR = 'params_error'
TEST_URL = 'https://testnet.bitmex.com/api'
TEST_API_KEY = 'RGJtLQbuBq3wM-igto8XxmIV'
TEST_SECRET_KEY = 'SOZfYnTXsIIpGdSEhpZieLxtCWFfXbj0BYvRmPvI_otA-Wtt'
API_KEY = '3l5O7-JZxilRTrmF2Hz4t6cG'
SECRET_KEY = '3_h4n0B6NMvoxaXb8XcraDj4FmiImLF3h9xWkmOwdmXMiBCh'


async def bitmex_future_get_order(api_key: str, secret_key: str, symbol: str, filters: str = None, columns: str = None,
                                  count: float = 100,
                                  start: float = None,
                                  reverse: bool = 'false', start_time: time = None, end_time: time = None, ):
    """
    查询订单
    :param api_key:
    :param secret_key:
    :param symbol:
    :param filters:
    :param columns:
    :param count:
    :param start:
    :param reverse:
    :param start_time:
    :param end_time:
    :return:
    """
    bitmex = BitMexFuture(api_key, secret_key, TEST_URL)
    return await bitmex.get_order(symbol, filters, columns, count, start, reverse, start_time, end_time)


async def bitmex_future_place_order(api_key: str, secret_key: str, symbol: str, order_side: str,
                                    simple_order_qty: float = None,
                                    order_qty: float = None,
                                    price: float = None,
                                    display_qty: float = None, stop_px: float = None, client_order_id: str = None,
                                    client_order_link_id: str = None,
                                    peg_offset_value: float = None,
                                    peg_price_type: str = None, order_type: str = None, time_in_force: str = None,
                                    execution_instructions: str = None,
                                    contingency_type: str = None,
                                    text: str = None):
    """
    下单
    :param api_key:
    :param secret_key:
    :param symbol:
    :param order_side:
    :param simple_order_qty:
    :param order_qty:
    :param price:
    :param display_qty:
    :param stop_px:
    :param client_order_id:
    :param client_order_link_id:
    :param peg_offset_value:
    :param peg_price_type:
    :param order_type:
    :param time_in_force:
    :param execution_instructions:
    :param contingency_type:
    :param text:
    :return:
    """
    bitmex = BitMexFuture(api_key, secret_key, TEST_URL)
    return await bitmex.post_order(symbol, order_side, simple_order_qty, order_qty, price, display_qty, stop_px,
                                   client_order_id, client_order_link_id, peg_offset_value, peg_price_type, order_type,
                                   time_in_force, execution_instructions, contingency_type, text)


async def bitmex_future_delete_order(api_key: str, secret_key: str, order_id: str = None, client_order_id: str = None,
                                     text: str = None):
    """
    撤销订单
    :param api_key:
    :param secret_key:
    :param order_id:
    :param client_order_id:
    :param text:
    :return:
    """
    if not order_id and not client_order_id:
        return PARAMS_ERROR

    bitmex = BitMexFuture(api_key, secret_key, TEST_URL)
    return await bitmex.delete_order(order_id, client_order_id, text)
