import asyncio
import base64
import datetime
import hashlib
import hmac
import logging
import urllib

from os.path import join

from crypto_exchange.utils.rest.api import APIClient
from crypto_exchange.utils.aio_http import aio_get, aio_post

logger = logging.getLogger(__name__)
PARAMS_ERROR = 'params_error'


class HuobiREST(APIClient):

    def __init__(self, api_key=None, secret_key=None, api_version="v1", url="https://api.huobi.pro"):
        self.api_key = api_key
        self.secret_key = secret_key
        self.url = url
        super(HuobiREST, self).__init__(url, api_version=api_version, api_key=api_key, secret_key=secret_key, )

    def sign(self, pParams: dict, method: str = None, host_url: str = None, request_path: str = None):
        sorted_params = sorted(pParams.items(), key=lambda d: d[0], reverse=False)
        encode_params = urllib.parse.urlencode(sorted_params)
        payload = [method, host_url, request_path, encode_params]
        payload = '\n'.join(payload)
        payload = payload.encode(encoding='UTF8')
        secret_key = self.secret_key.encode(encoding='UTF8')

        digest = hmac.new(secret_key, payload, digestmod=hashlib.sha256).digest()
        signature = base64.b64encode(digest)
        signature = signature.decode()
        return signature

    async def http_get(self, end_url: str, params: dict = None, headers: dict = None, sign=True):
        end_url = '/' + end_url
        method = 'GET'
        timestamp = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')
        params.update({'AccessKeyId': self.api_key,
                       'SignatureMethod': 'HmacSHA256',
                       'SignatureVersion': '2',
                       'Timestamp': timestamp})

        host_url = self.url
        host_name = urllib.parse.urlparse(host_url).hostname
        host_name = host_name.lower()
        params['Signature'] = self.sign(params, method, host_name, end_url)
        url = host_url + end_url
        # 添加请求头
        headers.update(
            {"Content-type": "application/x-www-form-urlencoded",
             'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/'
                           '537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36',
             }
        )
        # 异步
        # loop = asyncio.get_event_loop()
        # get_response = loop.run_until_complete(aio_get(url, params, headers=headers))

        return await aio_get(url, params, headers=headers)

    async def http_post(self, request_path: str, params: dict = None, headers: dict = None):
        # 加密拼接url
        request_path = '/' + request_path
        method = 'POST'
        timestamp = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')
        params_to_sign = {'AccessKeyId': self.api_key,
                          'SignatureMethod': 'HmacSHA256',
                          'SignatureVersion': '2',
                          'Timestamp': timestamp}

        host_url = self.url
        host_name = urllib.parse.urlparse(host_url).hostname
        host_name = host_name.lower()
        params_to_sign['Signature'] = self.sign(params_to_sign, method, host_name, request_path)
        url = host_url + request_path + '?' + urllib.parse.urlencode(params_to_sign)
        # 添加请求头

        headers = {
            "Accept": "application/json",
            'Content-Type': 'application/json'
        }
        # 事件循环对象
        # loop = asyncio.get_event_loop()
        # post_response = loop.run_until_complete(aio_post(url, json_data=params, headers=headers))
        return await aio_post(url, json_data=params, headers=headers)
