from typing import Awaitable

from websockets.client import WebSocketClientProtocol


class Client:
    def __init__(self, websocket: WebSocketClientProtocol) -> None:
        self._websocket = websocket

    async def wait_for_turn(self):
        # TODO wait until virus is done
        pass

    async def end_turn(self):
        # TODO sends a message to the server indicating end-of-turn
        pass
