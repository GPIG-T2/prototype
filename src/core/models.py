import re
from enum import Enum, auto
from typing import Any, Iterable, List, Tuple

# Define the type aliases
AreaId = int
TransportLinkId = int
PersonId = int
OrganisationId = int
RestrictionId = int


# Defined the enums
# To convert the int values back to the enum use "TransportKind(value)" so TransportKind(1) returns TransportKind.PATH
# Trying to convert a value which doesn't exist i.e. TransportKind(0) return a ValueError
class TransportKind(Enum):
    PATH = auto()
    TRAIN = auto()
    CAR = auto()
    BUS = auto()
    SUBWAY = auto()
    TRAM = auto()
    AIRPLANE = auto()


class OrganisationKind(Enum):
    SCHOOL = auto()
    HOSPITALITY = auto()
    RETAIL = auto()
    MEDICAL = auto()


class RestrictionStrictness(Enum):
    NONE = auto()
    MILD = auto()
    SEVERE = auto()


class Sex(Enum):
    MALE = auto()
    FEMALE = auto()


# Define the structures
def get_property_values(data: dict, props: Iterable[str]) -> List[Any]:
    return [data[prop] for prop in props]


def snake_case(strs: Iterable[str]) -> Iterable[str]:
    return [re.sub('([A-Z]+)', r'_\1', s).lower() for s in strs]


class DictObject:
    def to_dict(self, props: Iterable[str], attrs: Iterable[str]) -> dict:
        data: dict = {}
        for name in props:
            data[name] = getattr(self, name)
        return data


class PeopleData(DictObject):
    def __init__(self, total: int, infected: int, ids: List[PersonId]):
        self.total: int = total
        self.infected: int = infected
        self.ids: List[PersonId] = ids

    @staticmethod
    def from_dict(data: dict):
        pass

    def to_dict(self) -> dict:
        pass


class Area(DictObject):
    def __init__(self, id: AreaId, name: str, people: PeopleData, sub_areas: List[AreaId],
                 organisations: List[OrganisationId], transport_links: List[TransportLinkId], restriction_level: RestrictionStrictness):
        self.id: AreaId = id
        self.name: str = name
        self.people: PeopleData = people
        self.sub_areas: List[AreaId] = sub_areas
        self.organisations: List[OrganisationId] = organisations
        self.transport_links: List[TransportLinkId] = transport_links
        self.restriction_level: RestrictionStrictness = restriction_level

    @staticmethod
    def from_dict(data: dict):
        pass

    def to_dict(self) -> dict:
        pass


class TransportLink(DictObject):
    def __init__(self, id: TransportLinkId, kind: TransportKind, people: PeopleData, link: Tuple[AreaId, AreaId],
                 travel_time: float, restriction_level: RestrictionStrictness):
        self.id: TransportLinkId = id
        self.kind: TransportKind = kind
        self.people: PeopleData = people
        self.link: Tuple[AreaId, AreaId] = link
        self.travel_time: float = travel_time
        self.restriction_level: RestrictionStrictness = restriction_level

    @staticmethod
    def from_dict(data: dict):
        pass

    def to_dict(self) -> dict:
        pass


class AreaLayout(DictObject):
    def __init__(self, area_id: AreaId, x: float, y: float):
        self.area_id: AreaId = area_id
        self.x: float = x
        self.y: float = y

    @staticmethod
    def from_dict(data: dict):
        pass

    def to_dict(self) -> dict:
        pass


class Layout(DictObject):
    def __init__(self, areas: List[AreaId]):
        self.areas: List[AreaId] = areas

    @staticmethod
    def from_dict(data: dict):
        pass

    def to_dict(self) -> dict:
        pass


class Contact(DictObject):
    def __init__(self, person_id: PersonId, timestep: int):
        self.person_id: PersonId = person_id
        self.timestep: int = timestep

    @staticmethod
    def from_dict(data: dict):
        pass

    def to_dict(self) -> dict:
        pass


class Person(DictObject):
    def __init__(self, person_id: PersonId, age: int, sex: Sex):
        self.person_id: PersonId = person_id
        self.age: int = age
        self.sex: Sex = sex

    @staticmethod
    def from_dict(data: dict):
        pass

    def to_dict(self) -> dict:
        pass


class ContactTrace(DictObject):
    def __init__(self, person_id: PersonId, contact: List[Contact]):
        self.person_id: PersonId = person_id
        self.contact: List[Contact] = contact

    @staticmethod
    def from_dict(data: dict):
        pass

    def to_dict(self) -> dict:
        pass


class Organisation(DictObject):
    def __init__(self, organisation_id: OrganisationId, kind: OrganisationKind, people: PeopleData,
                 restriction_level: RestrictionStrictness):
        self.organisation_id: OrganisationId = organisation_id
        self.kind: OrganisationKind = kind
        self.people: PeopleData = people
        self.restriction_level: RestrictionStrictness = restriction_level

    @staticmethod
    def from_dict(data: dict):
        pass

    def to_dict(self) -> dict:
        pass


class Restriction(DictObject):
    def __init__(self, restriction_id: RestrictionId, restriction_level: RestrictionStrictness,
                 areas: List[AreaId], organisations: List[OrganisationId], transports: List[TransportLinkId]):
        self.restriction_id: RestrictionId = restriction_id
        self.restriction_level: RestrictionStrictness = restriction_level
        self.areas: List[AreaId] = areas
        self.organisations: List[OrganisationId] = organisations
        self.transports: List[TransportLinkId] = transports

    @staticmethod
    def from_dict(data: dict):
        pass

    def to_dict(self) -> dict:
        pass
