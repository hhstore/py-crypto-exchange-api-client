import asyncio
import logging
from abc import ABCMeta, abstractmethod

from os.path import join

from crypto_exchange.utils.aio_http import aio_get, aio_post, aio_get2, aio_post2

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
    def sign(self, params: dict, method: str = None, host_url: str = None, end_url: str = None):
        # TODO 该写点啥
        return

    async def http_get(self, end_url: str, query_params: dict = None, headers: dict = None):
        # 处理GET请求
        url = join(self.url, self.api_version, end_url)
        return await aio_get2(url, query_params, headers=headers)

    async def http_post(self, end_url: str, payload: dict = None, headers: dict = None):
        # 处理POST请求
        url = join(self.url, self.api_version, end_url)
        return await aio_post2(url, payload, headers=headers)
