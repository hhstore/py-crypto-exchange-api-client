import hashlib
import hmac
import logging
import time
import urllib

from crypto_exchange.utils.rest.api import APIClient

logger = logging.getLogger(__name__)


class BitMaxREST(APIClient):

    def __init__(self, api_key: str = None, secret_key: str = None, api_version: str = "v1",
                 url: str = "https://www.bitmex.com/api/v1"):
        super(BitMaxREST, self).__init__(url, api_version=api_version, api_key=api_key, secret_key=secret_key, )

    def sign(self, params: dict, method: str = None, host_url: str = None, end_url: str = None):
        parsed_url = urllib.parse.urlparse(host_url + end_url)
        path = parsed_url.path
        if parsed_url.query:
            path = path + '?' + parsed_url.query

        expires = int(time.time())

        message = bytes(method + path + str(expires) + str(params), 'utf-8')

        signature = hmac.new(bytes(self.secret_key, 'utf-8'), message, digestmod=hashlib.sha256).hexdigest()
        return signature
