from crypto_exchange.utils.websocket.okex_ws import OKexWSS


class OKexSpotWSClient(OKexWSS):

    def __init__(self, base_url="wss://real.okex.com:10441/websocket", api_key: str = '', secret_key: str = ''):
        """
        :param base_url:
        :param api_key:
        :param secret_key:
        """
        self.url = base_url
        super(OKexSpotWSClient, self).__init__(base_url, api_key, secret_key)

    async def ws_spot_ticker(self, symbol):
        """
        订阅行情数据
        :param symbol:
        :return:
        """
        params = "{'event':'addChannel','channel':'ok_sub_spot_%s_ticker'}" % symbol
        return await self.ws_app(self.url, params)

    async def ws_spot_depth(self, symbol):
        """
        订阅币币市场深度(200增量数据返回)
        :param symbol:
        :return:
        """
        params = "{'event':'addChannel','channel':'ok_sub_spot_%s_depth'}" % symbol
        return await self.ws_app(self.url, params)

    async def ws_spot_depth_size(self, symbol, size):
        """
        订阅市场深度
        :param symbol:
        :return:
        """
        params = "{'event':'addChannel','channel':'ok_sub_spot_%s_depth_%s'}" % (symbol, size)
        return await self.ws_app(self.url, params)

    async def ws_spot_deals(self, symbol):
        """
        订阅成交记录
        :param symbol:
        :return:
        """
        params = "{'event':'addChannel','channel':'ok_sub_spot_%s_deals'}" % symbol
        return await self.ws_app(self.url, params)

    async def ws_spot_k_line(self, symbol, k_line_type):
        """
        订阅K线数据
        :param symbol:
        :param k_line_type:
        :return:
        """
        params = "{'event':'addChannel','channel':'ok_sub_spot_X_kline_Y'}"
        return await self.ws_app(self.url, params)

    async def ws_spot_login(self):
        """
        login 登录事件(个人信息推送)
        :return:
        """
        params = {
            'api_key': self.api_key
        }
        sign = self.sign(params)
        params = """{"event":"login","parameters":{"api_key":"%s","sign":"%s"}}""" % (self.api_key, sign)
        return await self.ws_app(self.url, params)

    async def ws_spot_order(self, symbol):
        """
        交易数据
        :return:
        """
        params = "{'event':'addChannel','channel':'ok_sub_spot_%s_order'}" % symbol
        return await self.ws_app(self.url, params)

    async def ws_spot_balance(self,symbol):
        """
        账户信息
        :param symbol:
        :return:
        """
        params = "{'event':'addChannel','channel':'ok_sub_spot_%s_balance'}" % symbol
        return await self.ws_app(self.url, params)
