#!/usr/bin/env python3

# Way to reference the core folders
import pathlib
import sys
sys.path.insert(0, str(pathlib.Path().parent.absolute()) + "\\models")

import asyncio
from typing import Awaitable

import websockets
from client import Client
from who_model import Model

SERVER_URI = "ws://localhost:8765"


async def loop() -> Awaitable[None]:
    async with websockets.connect(SERVER_URI) as websocket:
        client = Client(websocket)
        model = Model(client)

        while model.is_running:
            await client.wait_for_turn()
            await model.tick()
            await client.end_turn()


def main() -> None:
    asyncio.get_event_loop().run_until_complete(loop())


if __name__ == "__main__":
    main()
