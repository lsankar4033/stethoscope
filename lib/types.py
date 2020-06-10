from typing import List, NamedTuple

from sclients import InstanceConfig


class Fixture(NamedTuple):
    name: str
    instances: List[InstanceConfig]
