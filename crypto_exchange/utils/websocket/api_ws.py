# Import Built-Ins
import aiohttp
import logging
from abc import ABCMeta, abstractmethod
from queue import Queue, Empty

import websockets

log = logging.getLogger(__name__)


class WSSAPI(metaclass=ABCMeta):
    """
    Base Class with no actual connection functionality. This is added in the
    subclass, as the various wss APIs are too diverse in order to distill a
    sensible pool of common attributes.
    """

    def __init__(self, base_url, api_key=None, secret_key=None, ):
        """

        :param base_url:
        :param api_key:
        :param secret_key:
        """
        log.debug("WSSAPI.__init__(): Initializing Websocket API")
        self.base_url = base_url
        self.api_key = api_key
        self.secret_key = secret_key
        # self.running = False

        # External Interface to interact with WSS.
        # self.interface = Queue()

        # Internal Command Queue for restarts, stops and starts
        # self._controller_q = Queue()

        # Queue storing all received data
        # self.data_q = Queue()

        # Internal Controller thread, responsible for starts / restarts / stops
        # self._controller_thread = None

    @abstractmethod
    def sign(self, params: dict, method: str = None, host_url: str = None, end_url: str = None):
        # TODO
        return




    def start(self):
        """
        Starts threads. Extend this in your child class.
        :return:
        """
        log.info("WSSAPI.start(): Starting Basic Facilities")
        self.running = True
        if self._controller_thread is None or not self._controller_thread.is_alive():
            self._controller_thread = Thread(target=self._controller,
                                             daemon=True,
                                             name='%s Controller Thread' %
                                                  self.name)
            self._controller_thread.start()

    def stop(self):
        """
        Stops Threads. Overwrite this in your child class as necessary.
        :return:
        """
        log.debug("WSSAPI.stop(): Stopping..")
        self.running = False

    def restart(self):
        """
        Restart Threads.
        :return:
        """
        log.debug("WSSAPI.restart(): Restarting API Client..")
        self.stop()
        self.start()

    def _controller(self):
        """
        This method runs in a dedicated thread, calling self.eval_command().
        :return:
        """
        while self.running:
            try:
                cmd = self._controller_q.get(timeout=1)
            except (TimeoutError, Empty):
                continue

            log.debug("WSSAPI._controller(): Received command: %s", cmd)
            Thread(target=self.eval_command, args=(cmd,)).start()

    def send(self, payload):
        """
        Method to send instructions for subcribing, unsubscribing, etc to
        the exchange API.
        :return:
        """
        raise NotImplementedError()

    def eval_command(self, cmd):
        """
        Evaluates commands issued by internal threads. Extend this as necessary.
        :param cmd:
        :return:
        """
        if cmd == 'restart':
            self.restart()

        elif cmd == 'stop':
            self.stop()

        else:
            raise ValueError("Unknown Command passed to controller! %s" % cmd)

    def get(self, **kwargs):
        return self.data_q.get(**kwargs)
