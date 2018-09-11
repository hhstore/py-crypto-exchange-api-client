import logging
from pprint import pprint

import pytest

from crypto_exchange.api.rest_api import place_order

logger = logging.getLogger(__name__)

OKEX_PUBLIC_KEY = '3b773537-bbae-4db9-9a9b-42069d7e1fbb'
OKEX_SECRET_KEY = 'EFAABB4F616059E45557329A86D2B77C'
HUOBI_PUBLIC_KEY = 'b313ab7a-7af2e128-ba036ea6-4acf6'
HUOBI_SECRET_KEY = 'eb60c766-702767da-3aaafaee-32381'


@pytest.mark.asyncio
async def test_huobi_rest_api():
    '''

    :return:{'data': '12115668178', 'status': 'ok'}
            {'data': None,
              'err-code': 'invalid-amount',
              'err-msg': 'Paramemter `amount` is invalid.',
              'status': 'error'}

            {'order_id': 7057629, 'result': True}
             {'error_code': 1007}
    '''
    # data = await place_order('huobi', HUOBI_PUBLIC_KEY, HUOBI_SECRET_KEY, 'spot', 'ncasheth',
    #                          spot_trade_type='buy-limit', price='0.0000002',
    #                          volume='1')

    # data = await place_order('okex', OKEX_PUBLIC_KEY, OKEX_SECRET_KEY, 'spot', '1st_eth', spot_trade_type='buy',
    #                          price='0.000005', volume='1')

    data = await place_order('okex', OKEX_PUBLIC_KEY, OKEX_SECRET_KEY, 'future', 'xrp', future_type='this_week',
                             future_trade_type='1', price='0.265', volume='1')
    pprint(data)
