#!/usr/bin/env python3
import asyncio
from typing import Awaitable

import websockets
from server import Server
from virus_model import Model
from websockets import WebSocketServerProtocol


async def loop(websocket: WebSocketServerProtocol, path: str) -> Awaitable[None]:
    model = Model()
    server = Server(websocket, model)

    while model.is_running:
        model.tick()
        await server.listen()


def main() -> None:
    server = websockets.serve(loop, "localhost", 8765)

    asyncio.get_event_loop().run_until_complete(server)
    asyncio.get_event_loop().run_forever()


if __name__ == "__main__":
    main()
