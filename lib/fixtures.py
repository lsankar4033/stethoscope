import eth_utils
import os
import subprocess
from typing import List

from sclients import SUPPORTED_CLIENTS, InstanceConfig, start_instance, stop_instance

from lib.types import Fixture

DEFAULT_INSTANCE_CONFIG = {
    'beacon_state_path': 'ssz/single_client_genesis.ssz',
    'enr': {
        'enr': 'enr:-LK4QJCIZoViytOOmAzAbdOJODwQ36PhjXwvXlTFTloTzpawVpvPRmtrM6UZdPmOGck5yPZ9AbgmwyZnE3jm4jX0Yx0Bh2F0dG5ldHOIAAAAAAAAAACEZXRoMpBGMkSJAAAAAf__________gmlkgnY0gmlwhH8AAAGJc2VjcDI1NmsxoQOnBq2PcxFfkFACZvJz91cd-UKaTPtLv7zYJSJyAtq60YN0Y3CCIyiDdWRwgiMp',
        'private_key': 'eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee',
        'udp': 9001,
        'tcp': 9000,
        'id': 'v4',
        'ip': '127.0.0.1',
        'attnets': '0x0000000000000000',
        'eth2': '0x4632448900000001ffffffffffffffff'
    }
}

def extract_fixtures(clients_to_test=SUPPORTED_CLIENTS) -> List[Fixture]:
    fixtures = []
    for client in SUPPORTED_CLIENTS:
        if client not in clients_to_test:
            continue

        instance_config = {
            **DEFAULT_INSTANCE_CONFIG,
            'client': client
        }

        fixture = Fixture(client, [InstanceConfig.from_dict(instance_config)])
        fixtures.append(fixture)

    return fixtures

def setup_fixture(fixture: Fixture):
    for instance in fixture.instances:
        if instance.client not in SUPPORTED_CLIENTS:
            raise ValueError(
                f"can't start instance: client {instance_config.client} not supported yet")

        start_instance(instance)


def teardown_fixture(fixture: Fixture):
    for instance in fixture.instances:
        stop_instance(instance.client)
