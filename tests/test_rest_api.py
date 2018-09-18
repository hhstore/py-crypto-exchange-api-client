import pytest

from crypto_exchange.api.rest_api import *

logger = logging.getLogger(__name__)

OKEX_PUBLIC_KEY = '3b773537-bbae-4db9-9a9b-42069d7e1fbb'
OKEX_SECRET_KEY = 'EFAABB4F616059E45557329A86D2B77C'
HUOBI_PUBLIC_KEY = 'b313ab7a-7af2e128-ba036ea6-4acf6'
HUOBI_SECRET_KEY = 'eb60c766-702767da-3aaafaee-32381'


@pytest.mark.asyncio
async def test_place_order():
    """

    :return:{'data': '12115668178', 'status': 'ok'}
            {'data': None,
              'err-code': 'invalid-amount',
              'err-msg': 'Paramemter `amount` is invalid.',
              'status': 'error'}

            {'order_id': 7057629, 'result': True}
             {'error_code': 1007}


             {'error_code': 20008, 'error_msg': '合约账户余额为空', 'status': 'error'}
             {'order_id': 1436472918752256, 'status': 'ok', 'status_code': 200}
    """

    # data = await spot_place_order('huobi', HUOBI_PUBLIC_KEY, HUOBI_SECRET_KEY, 'spot', 'ncasheth',
    #                               'bid', 'limit', price='0.0000002',
    #                               volume='1')

    data = await spot_place_order('okex', OKEX_PUBLIC_KEY, OKEX_SECRET_KEY, 'spot', 'auto_eth', 'bid','market',
                             price='0.00014', volume='1')
    #
    # data = await future_place_order('okex', OKEX_PUBLIC_KEY, OKEX_SECRET_KEY, 'future', 'xrp', 'bid',
    #                                 future_type='this_week',
    #                                 future_trade_type='1', price='0.254', volume='1')
    pprint(data)


@pytest.mark.asyncio
async def test_batch_place_orders():
    """
    {'order_info': [{'order_id': 11872081},
                    {'errorCode': '交易金额小于最小交易值', 'order_id': -1},
                    {'errorCode': '交易金额小于最小交易值', 'order_id': -1}],
     'status': True,
     'status_code': 200}
     {'err_msg': '没有交易市场信息', 'error_code': 1007, 'status': 'error'}


    {'order_info': [{'order_id': 1470131271963648},
                    {'error_code': 20012, 'order_id': -1},
                    {'error_code': 20012, 'order_id': -1}],
     'status': True,
     'status_code': 200}
     {'error_code': 20007, 'error_msg': '参数错误', 'status': 'error'}
    :return:
    """
    order_data = "[{price:0.00000551,amount:10,type:'buy'}," \
                 "{price:0.00000551,amount:10,type:'buy'}," \
                 "{price:0.00000551,amount:10,type:'buy'}]"
    data = await spot_batch_place_orders('okex', OKEX_PUBLIC_KEY, OKEX_SECRET_KEY, 'spot', 'show_eth', order_data,
                                         'bid')
    pprint('\n')
    pprint(data)

    # order_data = "[{price:0.270,amount:1,type:1,match_price:0}," \
    #              "{price:0.260,amount:1,type:1,match_price:0}," \
    #              "{price:0.250,amount:1,type:1,match_price:0}]"
    # data = await future_batch_place_orders('okex', OKEX_PUBLIC_KEY, OKEX_SECRET_KEY,
    #                                  'future','xrp', 'this_week', order_data,
    #                                  '10')
    # pprint('\n')
    # pprint(data)


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
    # data = await spot_cancel_order('okex',OKEX_PUBLIC_KEY,OKEX_SECRET_KEY,'spot','7057629','1st_eth',)
    # data = await spot_cancel_order('huobi', HUOBI_PUBLIC_KEY, HUOBI_SECRET_KEY, 'spot', '1186312514', )
    data = await future_cancel_order('okex', OKEX_PUBLIC_KEY, OKEX_SECRET_KEY, 'future', '1453287877917697',
                                     future_type='this_week', coin_type='xrp')
    pprint(data)


@pytest.mark.asyncio
async def test_batch_cancel_orders():
    """
    {'error': [''],
     'status': True,
     'status_code': 200,
     'success': ['7969464', '7969465', '7969466']}
    {'err_msg': '没有交易市场信息', 'error_code': 1007, 'status': 'error'}

    {'error': [],
     'status': 'ok',
     'status_code': 200,
     'success': ['12675565271', '12675631051', '12675644017', '12675655713']}


    {'err_msg': '必填参数为空', 'error_code': 20006, 'status': 'error'}
    {'error': ['1471104297421824:20015', '1471104297421825:20015'],
     'status': 'ok',
     'status_code': 200,
     'success': ['']}

    :return:
    """

    # data = await spot_batch_cancel_orders('okex',OKEX_PUBLIC_KEY,OKEX_SECRET_KEY,'spot','7970554','show_eth')
    # pprint(data)


    # data = await spot_batch_cancel_orders('huobi', HUOBI_PUBLIC_KEY, HUOBI_SECRET_KEY, 'spot',
    #                                       '12675565271,12675631051,12675644017,12675655713', 'ncasheth', )
    # pprint(data)

    # data = await future_batch_cancel_orders('okex',OKEX_PUBLIC_KEY,OKEX_SECRET_KEY,'future','1471104297421824,1471104297421825','xrp','this_week')
    # pprint(data)

@pytest.mark.asyncio
async def test_spot_order_info():
    """

    :return:
    """
    # data = await spot_order_info('okex',OKEX_PUBLIC_KEY,OKEX_SECRET_KEY,'spot','121863125','1st_eth')
    data = await future_order_info('okex', OKEX_PUBLIC_KEY, OKEX_SECRET_KEY, 'future', '1453287877917697', 'this_week',
                                   'xrp')
    pprint(data)


@pytest.mark.asyncio
async def test_depth():
    """
    深度
    :return:
    """
    pass
    # data = await


@pytest.mark.asyncio
async def test_withdraw():
    """
    提现
    :return:
    """
    pass


@pytest.mark.asyncio
async def test_cancel_withdraw():
    """
    取消提现
    :return:
    """
    pass


@pytest.mark.asyncio
async def test_balance():
    pass
