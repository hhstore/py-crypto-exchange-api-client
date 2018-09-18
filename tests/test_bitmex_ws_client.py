# -*- coding: utf-8 -*-
from crypto_exchange.exchanges.bitmex.bitmax_wsebsocket.bitmex_ws import BitMEXWebsocket
import logging
from time import sleep


# Basic use of websocket.
def run():

    # Instantiating the WS will make it connect. Be sure to add your api_key/api_secret.
    ws = BitMEXWebsocket(endpoint="wss://www.bitmex.com/realtime", symbol="XBTUSD",
                         api_key=None, api_secret=None)
    print("Instrument data: %s" % ws.get_instrument())

    # Run forever
    while(ws.ws.sock.connected):
        print("Ticker: %s" % ws.get_ticker())
        if ws.api_key:
            print("Funds: %s" % ws.funds())
        print("Market Depth: %s" % ws.market_depth())
        print("Recent Trades: %s\n\n" % ws.recent_trades())
        sleep(5)


def setup_logger():
    # Prints logger info to terminal
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)  # Change this to DEBUG if you want a lot more info
    ch = logging.StreamHandler()
    # create formatter
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    # add formatter to ch
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger


if __name__ == "__main__":
    run()
