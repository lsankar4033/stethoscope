from typing import List, NamedTuple


class ENR(NamedTuple):
    private_key: str
    tcp: int
    udp: int
    id: str
    ip: int
    enr: str
    attnets: str
    eth2: str


# NOTE: could turn into 'Instance' to represent a thing that can be on and turned off
class InstanceConfig(NamedTuple):
    client: str
    beacon_state_path: str
    enr: ENR

    @classmethod
    def from_dict(cls, d):
        return cls(d['client'], d['beacon_state_path'], ENR(**d['enr']))


class Fixture(NamedTuple):
    name: str
    instances: List[InstanceConfig]
