from pprint import pprint

from websocket import create_connection
import gzip
import time

if __name__ == '__main__':
    while True:
        try:
            ws = create_connection("wss://api.huobipro.com/ws")
            break
        except:
            print('connect ws error,retry...')
            time.sleep(5)

    # 订阅 KLine 数据
    tradeStr = """{"sub": "market.ethusdt.kline.1min","id": "id10"}"""

    ws.send(tradeStr)
    while True:
        compressData = ws.recv()
        result = gzip.decompress(compressData).decode('utf-8')
        pprint(result)
        if result[:7] == '{"ping"':
            ts = result[8:21]
            pong = '{"pong":' + ts + '}'
            ws.send(pong)
            ws.send(tradeStr)
        else:
            pprint(result)
