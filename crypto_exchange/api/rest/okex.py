import hashlib
import logging


from crypto_exchange.api.rest.api import APIClient

logger = logging.getLogger(__name__)


class OKExREST(APIClient):

    def __init__(self, api_key=None, secret_key=None, api_version="v1", url="https://www.okex.com/api"):

        super(OKExREST, self).__init__(url, api_version=api_version, api_key=api_key, secret_key=secret_key, )

    def sign(self, params:dict, ):
        sign = ''
        # secret_key = secret_key if secret_key else SECRETKEY
        # 对参数进行排序,拼接数据
        for key in sorted(params.keys()):
            sign += key + "=" + str(params[key]) + "&"
        data = sign + "secret_key=" + self.secret_key
        # 签名
        return hashlib.md5(data.encode("utf8")).hexdigest().upper()

