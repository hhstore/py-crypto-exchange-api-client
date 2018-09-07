from pprint import pprint

import websocket
try:
    import thread
except ImportError:
    import _thread as thread
import time


def on_message(ws, message):
    print('接收数据')
    print(message)


def on_error(ws, error):
    print(error)


def on_close(ws):
    print("连接关闭")


def on_open(ws):
    def run(*args):
        for i in range(3):
            time.sleep(1)
            ws.send("Hello %d" % i)
        time.sleep(1)
        ws.close()
        print("thread terminating...")
    thread.start_new_thread(run, ())


def send():
    pass


if __name__ == "__main__":

    ws = websocket.create_connection('wss://real.okex.com:10441/websocket')
    ws.send("{'event':'addChannel','channel':'ok_sub_spot_bch_btc_ticker'}")
    data=ws.recv()
    pprint(data)
    ws.close()


