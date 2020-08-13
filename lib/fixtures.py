import eth_utils
import os
import subprocess
from typing import List

from sclients import SUPPORTED_CLIENTS, InstanceConfig, start_instance, stop_instance

from lib.instance_configs import DEFAULT_INSTANCE_CONFIG
from lib.types import Fixture

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
        start_instance(instance)


def teardown_fixture(fixture: Fixture):
    for instance in fixture.instances:
        stop_instance(instance.client)
