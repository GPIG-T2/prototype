import json
from typing import Awaitable

from virus_model import Model
from websockets.server import WebSocketServerProtocol


class Server:
    def __init__(self, websocket: WebSocketServerProtocol, model: Model) -> None:
        self._websocket = websocket
        self._model = model

    async def listen(self) -> Awaitable[None]:
        async for message in self._websocket:
            data = json.loads(message)

            if data["kind"] == "done":
                break
