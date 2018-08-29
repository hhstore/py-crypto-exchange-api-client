from json import JSONDecodeError

import aiohttp
import async_timeout

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
    headers = headers.update(default_headers) if headers else default_headers

    async with aiohttp.ClientSession() as session:
        with async_timeout.timeout(10):
            async with session.get(url=url, headers=headers, params=query_params) as response:
                return parse_response(response=response)


async def aio_post(url: str, payload: dict = None, headers: dict = None):
    """ HTTP POST:

    :param url:
    :param payload:
    :param headers:
    :return:
    """
    default_headers = {"User-Agent": UA_FIREFOX, }
    headers = headers.update(default_headers) if headers else default_headers

    async with aiohttp.ClientSession() as session:
        with async_timeout.timeout(10):
            async with session.post(url=url, headers=headers, data=payload) as response:
                return parse_response(response=response)


def parse_response(response):
    """格式化返回值

    :param response:
    :return:
    """
    status_code = response.status
    is_ok = bool(200 <= status_code <= 206)

    try:
        result = response.json()
    except JSONDecodeError as e:
        logger.error(f"Not Json Format {e}")
        result = response.text()
    return is_ok, status_code, response, result
