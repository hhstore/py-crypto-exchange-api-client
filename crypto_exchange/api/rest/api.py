import asyncio
import logging
import time
from abc import ABCMeta, abstractmethod
from os.path import join

from crypto_exchange.utils.aio_http import aio_get, aio_post

logger = logging.getLogger(__name__)


class APIClient(metaclass=ABCMeta):
    """

    """

    def __init__(self, url, api_version=None, api_key=None, secret_key=None, ):
        # TODO 初始化参数
        self.api_version = api_version
        self.url = url
        self.api_key = api_key
        self.secret_key = secret_key
        pass

    @abstractmethod
    def sign(self, params, ):
        # TODO 该写点啥
        return

    def http_get(self, end_url, query_params, headers=None):
        # 处理GET请求
        url = join(self.url, self.api_version, end_url)
        query_params = query_params

        loop = asyncio.get_event_loop()
        get_response = loop.run_until_complete(aio_get(url, query_params, headers=headers))

        return get_response

    def http_post(self, end_url, payload, headers=None):
        # 处理POST请求
        url = join(self.url, self.api_version, end_url)
        payload = payload
        # 事件循环对象
        loop = asyncio.get_event_loop()
        post_response = loop.run_until_complete(aio_post(url, payload, headers=headers))
        return post_response
