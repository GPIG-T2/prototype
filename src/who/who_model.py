from client import Client
from typing import List, Union, Dict

from core.models import Area, AreaId, Layout, Organisation, OrganisationId, TransportLink, TransportLinkId


class Model:
    def __init__(self, client: Client) -> None:
        self._client = client
        self.layout: Union[None, Layout] = None
        self.areas: Dict[AreaId, Area] = {}
        self.transport_links: Dict[TransportLinkId, TransportLink] = {}
        self.organisations: Dict[OrganisationId, Organisation] = {}

    async def tick(self) -> None:
        if self.layout is None:
            await self.populate_initial_data()

    async def populate_initial_data(self) -> None:
        # Returns a layout which contains all the area ids
        self.layout = await self.get_layout()

        # Get all the areas
        areas = await self.get_areas(self.layout.areas)

        area: Area
        for area in areas:
            self.areas[area.area_id] = area

        # Get all the transport links
        area: Area
        for area in self.areas.values():
            self.load_area_information(area)

    async def load_area_information(self, area: Area):

        transport_link_ids_to_request = list()

        transport_id: TransportLinkId
        for transport_id in area.transport_links:
            if transport_id not in self.transport_links.keys():
                transport_link_ids_to_request.append(transport_id)

        transports = await self.get_transports(transport_link_ids_to_request)

        transport: TransportLink
        for transport in transports:
            self.transport_links[transport.link_id] = transport

        organisation_ids_to_request = list()

        organisation_id: OrganisationId
        for organisation_id in area.organisations:
            if organisation_id not in self.organisations.keys():
                organisation_ids_to_request.append(organisation_id)

        organisations = await self.get_organisations(organisation_ids_to_request)

        organisation: Organisation
        for organisation in organisations:
            self.organisations[organisation.organisation_id] = organisation

    async def get_organisations(self, organisation_ids: List[OrganisationId]) -> List[Organisation]:
        pass  # path: organisations, ids = [organisation_id]

    async def get_layout(self) -> Layout:
        pass

    async def get_areas(self, area_ids: List[AreaId]) -> List[Area]:
        pass

    async def get_transports(self, transport_ids: List[TransportLinkId]) -> List[TransportLink]:
        pass

    @property
    def is_running(self) -> bool:
        # TODO caclulate this on the fly when model is implemented
        return False
