# -*- coding: utf-8 -*-


# ******************* kline cycle ****************************
class KlineCycle:

    KLine1Min = 1
    KLine3Min = 2
    KLine5Min = 3
    KLine15Min = 4
    KLine30Min = 5
    KLine1hour = 6
    KLine4hour = 7
    KLineDay = 8
    KLine5Day = 9
    KLineWeek = 10
    KLineMonth = 11
    KLineYear = 12


class OKCycle:

    CYCLE = {
        "1min": KlineCycle.KLine1Min,
        "3min": KlineCycle.KLine3Min,
        "5min": KlineCycle.KLine5Min,
        "15min": KlineCycle.KLine15Min,
        "30min": KlineCycle.KLine30Min,
        "1hour": KlineCycle.KLine1hour,
        "2hour": 0,
        "4hour": KlineCycle.KLine4hour,
        "6hour": 0,
        "12hour": 0,
        "day": KlineCycle.KLineDay,
        "3day": 0,
        "week": KlineCycle.KLineWeek,
    }

    @property
    def cycles(self):
        periods = []
        for k, v in self.CYCLE.items():
            if v == 0:
                continue
            periods.append(k)
        return periods

    def get_cycle_value(self, cycle: str):
        if cycle in self.cycles:
            return True, self.CYCLE.get(cycle)
        return False, None


class HuoBiCycle:

    CYCLE = {
        "1min": KlineCycle.KLine1Min,
        "5min": KlineCycle.KLine5Min,
        "15min": KlineCycle.KLine15Min,
        "30min": KlineCycle.KLine30Min,
        "60min": KlineCycle.KLine1hour,
        "1day": KlineCycle.KLineDay,
        "1mon": KlineCycle.KLineMonth,
        "1week": KlineCycle.KLineWeek,
        "1year": KlineCycle.KLineYear,
    }

    @property
    def cycles(self):
        periods = []
        for k, v in self.CYCLE.items():
            if v == 0:
                continue
            periods.append(k)
        return periods

    def get_cycle_value(self, cycle: str):
        if cycle in self.cycles:
            return True, self.CYCLE.get(cycle)
        return False, None


class BitMexCycle:

    CYCLE = {
        "1m": KlineCycle.KLine1Min,
        "5m": KlineCycle.KLine5Min,
        "1h": KlineCycle.KLine1hour,
        "1d": KlineCycle.KLineDay,
    }

    @property
    def cycles(self):
        periods = []
        for k, v in self.CYCLE.items():
            if v == 0:
                continue
            periods.append(k)
        return periods

    def get_cycle_value(self, cycle: str):
        if cycle in self.cycles:
            return True, self.CYCLE.get(cycle)
        return False, None


# ************************* USDT 交易对 ************************
COMMON_USDT = ["USDT_BTC", "USDT_ETH", "USDT_EOS", "USDT_BCH", "USDT_XRP", "USDT_ETC", "USDT_LTC", "USDT_NEO",
               "USDT_TRX", "USDT_DASH", "USDT_ZEC", "USDT_IOTA", "USDT_IOST", "USDT_OMG"]

OK_USDT = ["USDT_XLM", "USDT_XMR", "USDT_ONT", "USDT_ADA", "USDT_OKB"]

HUOBI_USDT = ["USDT_ONT", "USDT_ADA", "USDT_HT"]


# ************************* BTC交易对 **************************
COMMON_BTC = ["BTC_ETH", "BTC_EOS", "BTC_BCH", "BTC_XRP", "BTC_ETC", "BTC_LTC", "BTC_NEO", "BTC_TRX", "BTC_DASH",
              "BTC_XLM", "BTC_ZEC", "BTC_XMR", "BTC_IOTA", "BTC_OMG", "BTC_IOST"]

OK_BTC = ["BTC_ONT", "BTC_ADA", "BTC_OKB"]

HUOBI_BTC = ["BTC_ONT", "BTC_ADA", "BTC_HT"]


# ************************* ETH交易对 **************************
COMMON_ETH = ["ETH_EOS", "ETH_TRX", "ETH_XLM", "ETH_IOTA", "ETH_IOST", "ETH_OMG"]

OK_ETH = ["ETH_ETC", "ETH_LTC", "ETH_NEO", "ETH_BCH", "ETH_XMR", "ETH_ONT", "ETH_ADA", "ETH_XRP", "ETH_DASH",
          "ETH_ZEC", "ETH_OKB"]
HUOBI_ETH = ["ETH_XMR", "ETH_ONT", "ETH_ADA", "ETH_HT"]

# ************************* HT交易对 ***************************
COMMON_HT = []

OK_HT = ["HT_EOS", "HT_BCH", "HT_XRP", "HT_ETC", "HT_LTC", "HT_DASH", "HT_NEO", "HT_TRX", "HT_ZEC", "HT_IOTA", "HT_ADA"]

HUOBI_HT = ["HT_EOS", "HT_BCH", "HT_XRP", "HT_ETC", "HT_LTC", "HT_DASH", "HT_IOST"]


# ************************* bitmex 永续合约 *********************
BITMEX_YX = ["XBTUSD", "ETHUSD"]

# ************************* bitmex 定期合约 *********************
BITMEX_DQ = ["ADA", "BCH", "EOS", "LTC", "TRX", "XRP"]


class OKexSymbol:

    USDT = COMMON_USDT + OK_USDT

    BTC = COMMON_BTC + OK_BTC

    ETH = COMMON_ETH + OK_ETH

    HT = COMMON_HT + OK_HT

    @property
    def usdt_symbol(self):
        return [symbol.lower() for symbol in self.USDT]

    @property
    def btc_symbol(self):
        return [symbol.lower() for symbol in self.BTC]

    @property
    def eth_symbol(self):
        return [symbol.lower() for symbol in self.ETH]

    @property
    def ht_symbol(self):
        if self.HT:
            return [symbol.lower() for symbol in self.HT]
        return []

    @property
    def symbols(self):
        return self.USDT + self.BTC + self.ETH + self.HT

    def symbol_transfer(self, symbol: str):
        if symbol in self.symbols:
            return True, symbol.upper()
        return False, None


class HuoBiSymbol:

    USDT = COMMON_USDT + HUOBI_USDT
    BTC = COMMON_BTC + HUOBI_BTC
    ETH = COMMON_ETH + HUOBI_ETH
    HT = COMMON_HT + HUOBI_HT

    @property
    def usdt_symbol(self):
        return [symbol.replace('_', '').lower() for symbol in self.USDT]

    @property
    def btc_symbol(self):
        return [symbol.replace('_', '').lower() for symbol in self.BTC]

    @property
    def eth_symbol(self):
        return [symbol.replace('_', '').lower() for symbol in self.ETH]

    @property
    def ht_symbol(self):
        return [symbol.replace('_', '').lower() for symbol in self.HT]

    @property
    def symbols(self):
        return self.usdt_symbol + self.btc_symbol + self.eth_symbol + self.ht_symbol

    def symbol_transfer(self, symbol: str):
        if symbol in self.usdt_symbol:
            return True, (symbol[0:4] + '_' + symbol[4:]).upper()

        if symbol in self.btc_symbol or symbol in self.eth_symbol:
            return True, (symbol[0:3] + '_' + symbol[3:]).upper()

        if symbol in self.ht_symbol:
            return True, (symbol[0:2] + '_' + symbol[2:]).upper()
        return False, None


class BitMexSymbol:

    YX = BITMEX_YX
    DQ = BITMEX_DQ

    def symbol_transfer(self, symbol: str):

        if symbol in self.YX:
            return True, (symbol[:-3] + '_' + symbol[-3:]).replace('XBT', 'BTC')

        return False, None


if __name__ == '__main__':
    print(OKCycle.CYCLE)
    print(OKCycle().cycles)
