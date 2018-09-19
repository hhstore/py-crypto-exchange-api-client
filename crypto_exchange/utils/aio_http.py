import json
import time
from json import JSONDecodeError

import aiohttp
import async_timeout
import requests

from .logging import get_logger

logger = get_logger(__name__)

# user-agent:
UA_IPHONE = "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0_1 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A402 Safari/604.1"
UA_ANDROID = "Mozilla/5.0 (Linux; Android 7.0; PLUS Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.98 Mobile Safari/537.36"
UA_FIREFOX = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:57.0) Gecko/20100101 Firefox/57.0"


async def aio_get(url: str, query_params: dict = None, headers: dict = None):
    """ HTTP GET:

    :param url:
    :param query_params:
    :param headers:
    :return:
    """
    default_headers = {"User-Agent": UA_FIREFOX, }
    if headers:
        headers.update(default_headers)
    else:
        headers = default_headers

    async with aiohttp.ClientSession() as session:
        with async_timeout.timeout(10):
            async with session.get(url=url, headers=headers, params=query_params) as response:
                try:
                    result = await response.json(content_type=None)
                except JSONDecodeError as e:
                    logger.error(f"Not Json Format {e}")
                    result = await response.text()
                return await parse_response(response=response, result=result)


async def aio_get2(url: str, query_params: dict = None, headers: dict = None):
    """ HTTP GET:

    :param url:
    :param query_params:
    :param headers:
    :return:
    """
    default_headers = {"User-Agent": UA_FIREFOX, }
    if headers:
        headers.update(default_headers)
    else:
        headers = default_headers
    async with aiohttp.ClientSession() as session:
        with async_timeout.timeout(10):
            async with session.get(url=url, headers=headers, params=query_params) as response:
                return await response.json()


async def aio_post2(url: str, payload: dict = None, headers: dict = None):
    """ HTTP POST:

    :param url:
    :param payload:
    :param headers:
    :return:
    """
    default_headers = {"User-Agent": UA_FIREFOX, }
    if headers:
        headers.update(default_headers)
    else:
        headers = default_headers

    async with aiohttp.ClientSession() as session:
        with async_timeout.timeout(10):
            async with session.post(url=url, headers=headers, json=payload) as response:
                return await response.json(content_type=None)


async def aio_post(url: str, payload: dict = None, json_data: dict = None, headers: dict = None):
    """ HTTP POST:

    :param url:
    :param payload:
    :param json_data:
    :param headers:
    :return:
    """
    default_headers = {"User-Agent": UA_FIREFOX, }
    if headers:
        headers.update(default_headers)
    else:
        headers = default_headers

    async with aiohttp.ClientSession() as session:
        with async_timeout.timeout(10):
            async with session.post(url=url, headers=headers, data=payload, json=json_data) as response:
                try:
                    # 禁用JSON响应的内容类型验证
                    result = await response.json(content_type=None)
                except JSONDecodeError as e:
                    logger.error(f"Not Json Format {e}")
                    result = await response.text()
                return await parse_response(response=response, result=result)


async def aio_delete(url: str, payload: dict = None, json_data: dict = None, headers: dict = None):
    """
    HTTP DELETE
    :param url:
    :param payload:
    :param json_data:
    :param headers:
    :return:
    """
    default_headers = {"User-Agent": UA_FIREFOX, }
    if headers:
        headers.update(default_headers)
    else:
        headers = default_headers
    async with aiohttp.ClientSession() as session:
        async with session.delete(url=url, data=payload, json=json_data, headers=headers) as response:
            try:
                result = await response.json(content_type=None)
            except Exception as e:
                logger.error(e)
                result = await response.text()
            return await parse_response(response=response, result=result)


async def aio_put(url: str, payload: dict = None, json_data: dict = None, headers: dict = None):
    """
    HTTP PUT
    :param url:
    :param payload:
    :param json_data:
    :param headers:
    :return:
    """
    default_headers = {"User-Agent": UA_FIREFOX, }
    if headers:
        headers.update(default_headers)
    else:
        headers = default_headers
    async with aiohttp.ClientSession() as session:
        async with session.put(url=url, data=payload, json=json_data, headers=headers) as response:
            try:
                result = await response.json(content_type=None)
            except Exception as e:
                logger.error(e)
                result = await response.text()
            return await parse_response(response=response, result=result)


async def parse_response(response, result):
    """格式化返回值

    :param response:
    :param result
    :return:
    """
    status_code = response.status
    is_ok = bool(200 <= status_code <= 206)

    # try:
    #     result = response.json()
    # except JSONDecodeError as e:
    #     logger.error(f"Not Json Format {e}")
    #     result = response.text()
    return is_ok, status_code, response, result
