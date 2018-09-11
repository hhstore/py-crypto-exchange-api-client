import logging
from pprint import pprint

import pytest

from crypto_exchange.api.rest_api import place_order, cancel_order

logger = logging.getLogger(__name__)

OKEX_PUBLIC_KEY = '3b773537-bbae-4db9-9a9b-42069d7e1fbb'
OKEX_SECRET_KEY = 'EFAABB4F616059E45557329A86D2B77C'
HUOBI_PUBLIC_KEY = 'b313ab7a-7af2e128-ba036ea6-4acf6'
HUOBI_SECRET_KEY = 'eb60c766-702767da-3aaafaee-32381'


@pytest.mark.asyncio
async def test_place_order():
    '''

    :return:{'data': '12115668178', 'status': 'ok'}
            {'data': None,
              'err-code': 'invalid-amount',
              'err-msg': 'Paramemter `amount` is invalid.',
              'status': 'error'}

            {'order_id': 7057629, 'result': True}
             {'error_code': 1007}


             {'error_code': 20008, 'error_msg': '合约账户余额为空', 'status': 'error'}
             {'order_id': 1436472918752256, 'status': 'ok', 'status_code': 200}
    '''
    # data = await place_order('huobi', HUOBI_PUBLIC_KEY, HUOBI_SECRET_KEY, 'spot', 'ncasheth',
    #                          'bid', 'limit', price='0.0000002',
    #                          volume='1')

    # data = await place_order('okex', OKEX_PUBLIC_KEY, OKEX_SECRET_KEY, 'spot', '1st_eth', 'bid','limit',
    #                          price='0.000005', volume='1')

    data = await place_order('okex', OKEX_PUBLIC_KEY, OKEX_SECRET_KEY, 'future', 'xrp', 'bid', future_type='this_week',
                             future_trade_type='1', price='0.254', volume='1')
    pprint(data)


@pytest.mark.asyncio
async def test_cancel_order():
    """

    :return:{'err_msg': '没有订单', 'error_code': 1009, 'result': 'False', 'status': 'error'}
            {'order_id': '7076647', 'result': True, 'status': 'ok', 'status_code': 200}

            {'err_msg': 'the order state is error','error_code': 'order-orderstate-error','status': 'error'}
            {'order_id': '12186312514','result': 'True','status': 'ok','status_code': 200}

            {'err_msg': '密钥不存在', 'error_code': 20020, 'status': 'error'}
            {'order_id': '1436550250372096','result': True,'status': 'ok','status_code': 200}
    """
    # data = await cancel_order('okex',OKEX_PUBLIC_KEY,OKEX_SECRET_KEY,'spot','7057629','1st_eth',)
    # data = await cancel_order('huobi', HUOBI_PUBLIC_KEY, HUOBI_SECRET_KEY, 'spot', '1186312514', )
    data = await cancel_order('okex', OKEX_PUBLIC_KEY, OKEX_SECRET_KEY, 'future', '1436550250372096',
                              future_type='this_week', coin_type='xrp')
    pprint(data)
