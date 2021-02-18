from typing import Awaitable

from websockets.client import WebSocketClientProtocol
from json import dumps

END_TURN_MESSAGE = dumps({"kind": "FINISHED"})


class Client:
    def __init__(self, websocket: WebSocketClientProtocol) -> None:
        self._websocket = websocket

    async def wait_for_turn(self):
        await self._websocket.recv()

    async def end_turn(self):
        await self._websocket.send(END_TURN_MESSAGE)
