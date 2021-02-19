from json import dumps, loads
from typing import List

from websockets.client import WebSocketClientProtocol

from core.messages import END_TURN_MESSAGE
from core.models import (Area, AreaId, Layout, Organisation, OrganisationId,
                         TransportLink, TransportLinkId)


class Client:
    def __init__(self, websocket: WebSocketClientProtocol) -> None:
        self._websocket = websocket
        self._cnonce = 0

    async def wait_for_turn(self):
        await self._websocket.recv()

    async def end_turn(self):
        await self._websocket.send(dumps(END_TURN_MESSAGE))

    async def get_organisations(self, organisation_ids: List[OrganisationId]) -> List[Organisation]:
        orgs = await self._get("organisations", organisation_ids)
        return [Organisation.from_dict(org) for org in orgs]

    async def get_layout(self) -> Layout:
        layout = await self._get("layout", [])
        return [Layout.from_dict(l) for l in layout]

    async def get_areas(self, area_ids: List[AreaId]) -> List[Area]:
        areas = await self._get("organisations", area_ids)
        return [Area.from_dict(area) for area in areas]

    async def get_transport_links(self, transport_ids: List[TransportLinkId]) -> List[TransportLink]:
        links = await self._get("links", transport_ids)
        return [TransportLink.from_dict(link) for link in links]

    async def _get(self, path: str, ids: List[int]) -> List:
        return await self._request({
            "kind": "get",
            "path": path,
            "ids": ids
        })

    async def _request(self, msg: dict) -> List:
        cnonce = str(self._cnonce)
        msg["nonce"] = cnonce

        self._cnonce += 1

        await self._websocket.send(dumps(msg))
        res = await self._websocket.recv()
        response = loads(res)

        if response["data"] is None:
            err = loads(response["error"])
            raise Exception(err["reason"])

        if response["nonce"] != cnonce:
            raise Exception("Got back unexpected nonce from server")

        data = loads(response["data"])

        return data
