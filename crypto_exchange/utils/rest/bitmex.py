import hashlib
import hmac
import logging
import time
import json as js
import urllib
from os.path import join

from crypto_exchange.utils.aio_http import aio_get, aio_post, aio_delete
from crypto_exchange.utils.rest.api import APIClient

logger = logging.getLogger(__name__)


class BitMexREST(APIClient):

    def __init__(self, api_key: str = None, secret_key: str = None, api_version: str = "v1",
                 url: str = "https://www.bitmex.com/api"):
        self.api_version = api_version
        super(BitMexREST, self).__init__(url, api_version=api_version, api_key=api_key, secret_key=secret_key, )

    async def sign(self, params: dict, method: str = None, host_url: str = None, end_url: str = None,
                   expires: str = None):
        # verb = 'POST'
        # path = '/api/v1/order'
        # expires = 1518064238 # 2018-02-08T04:30:38Z
        # data = '{"symbol":"XBTM15","price":219.0,"clOrdID":"mm_bitmex_1a/oemUeQ4CAJZgP3fjHsA","orderQty":98}'

        # verb = 'GET'
        # # Note url-encoding on querystring - this is '/api/v1/instrument?filter={"symbol": "XBTM15"}'
        # # Be sure to HMAC *exactly* what is sent on the wire
        # path = '/api/v1/instrument?filter=%7B%22symbol%22%3A+%22XBTM15%22%7D'
        # expires = 1518064237  # 2018-02-08T04:30:37Z
        # data = ''

        end_url = '/' + self.api_version + '/' + end_url
        parsed_url = urllib.parse.urlparse(host_url + end_url)
        path = parsed_url.path

        if parsed_url.query:
            path = path + '?' + parsed_url.query

        if method == 'GET':
            path = path + '?' + urllib.parse.urlencode(params)
            data = ''
            message = method + path + expires + data
        else:
            message = method + path + expires + js.dumps(params)

        return hmac.new(bytes(self.secret_key, 'utf-8'), bytes(message, 'utf-8'), digestmod=hashlib.sha256).hexdigest()

    async def http_get(self, end_url: str, query_params: dict = None, headers: dict = None):
        # 处理GET请求
        url = join(self.url, self.api_version, end_url)

        return await aio_get(url, query_params, headers=headers)

    async def http_post(self, end_url: str, payload: dict = None, headers: dict = None):
        # 处理POST请求
        url = join(self.url, self.api_version, end_url)

        return await aio_post(url, json_data=payload, headers=headers)

    async def http_delete(self, end_url: str, query_params: dict = None, headers: dict = None):
        # 处理DELETE请求
        url = join(self.url, self.api_version, end_url)

        return await aio_delete(url, json_data=query_params, headers=headers)
