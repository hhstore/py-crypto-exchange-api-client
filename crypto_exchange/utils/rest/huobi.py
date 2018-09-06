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
        super(HuobiREST, self).__init__(url, api_version=api_version, api_key=api_key, secret_key=secret_key, )

    def sign(self, params: dict, method: str = None, host_url: str = None, end_url: str = None):
        if method and host_url and end_url:
            sign = ''
            # 对参数进行排序,拼接数据
            for key in sorted(params.keys()):
                sign += key + "=" + str(params[key]) + "&"

            payload = [method, host_url, end_url, sign]
            payload = '\n'.join(payload)
            # 编码加密
            payload = payload.encode(encoding='UTF8')
            secret_key = self.secret_key.encode(encoding='UTF8')
            digest = hmac.new(secret_key, payload, digestmod=hashlib.sha256).digest()
            signature = base64.b64encode(digest)
            signature = signature.decode()
            return signature
            # host_url = "api.huobi.pro"
            # sorted_params = sorted(params.items(), key=lambda d: d[0], reverse=False)
            # encode_params = urllib.parse.urlencode(sorted_params)
            # payload = [method, host_url, end_url, encode_params]
            # payload = '\n'.join(payload)
            # payload = payload.encode(encoding='utf-8')
            # secret_key = self.secret_key.encode(encoding='utf-8')
            #
            # digest = hmac.new(secret_key, payload, digestmod=hashlib.sha256).digest()
            # signature = base64.b64encode(digest)
            # signature = signature.decode()
            # return signature
        else:
            return PARAMS_ERROR

    def http_get(self, end_url: str, query_params: dict = None, headers: dict = {}, sign=True):
        method = 'GET'
        timestamp = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')
        if sign:
            # 加密
            query_params.update({'AccessKeyId': self.api_key,
                                 'SignatureMethod': 'HmacSHA256',
                                 'SignatureVersion': '2',
                                 'Timestamp': timestamp})
            query_params['Signature'] = self.sign(query_params, method, self.url, end_url)
        url = join(self.url, end_url)
        # 添加请求头
        headers.update(
            {"Content-type": "application/x-www-form-urlencoded",
             'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/'
                           '537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36',
             }
        )
        # 异步
        loop = asyncio.get_event_loop()
        get_response = loop.run_until_complete(aio_get(url, query_params, headers=headers))

        return get_response

    def http_post(self, end_url: str, payload: dict = None, headers: dict = {}):
        method = 'POST'
        timestamp = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')
        # 加密拼接url
        sign_params = {'AccessKeyId': self.api_key,
                       'SignatureMethod': 'HmacSHA256',
                       'SignatureVersion': '2',
                       'Timestamp': timestamp, }
        sign_params['Signature'] = self.sign(sign_params, method, self.url, end_url)
        url = join(self.url, end_url) + '?' + urllib.parse.urlencode(sign_params)
        # 添加请求头
        headers.update({
            "Accept": "application/json",
            'Content-Type': 'application/json'
        })
        # 事件循环对象
        loop = asyncio.get_event_loop()
        post_response = loop.run_until_complete(aio_post(url, payload, headers=headers))
        return post_response
