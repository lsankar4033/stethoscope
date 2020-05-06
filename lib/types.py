from typing import NamedTuple


class ENR(NamedTuple):
    private_key: str
    tcp: int
    udp: int
    ip: int
    enr: str
    attnets: str
    eth2: str


class InstanceConfig(NamedTuple):
    client: str
    beacon_state_path: str
    enr: ENR

    @classmethod
    def from_dict(cls, d):
        return cls(d['client'], d['beacon_state_path'], ENR(**d['enr']))
