import eth_utils
import os
import subprocess
from typing import List

from sclients import SUPPORTED_CLIENTS, InstanceConfig, start_instance, stop_instance

from lib.types import Fixture


def extract_fixtures(config, clients_to_test=SUPPORTED_CLIENTS) -> List[Fixture]:
    # turn a yml config into a list of fixtures. if any 'all' in the file, do 1:1 for every one (rather than all
    # pairwise combos)
    if any((i['client'] == 'all' for i in config['instances'])):
        fixtures = []

        for client in SUPPORTED_CLIENTS:
            if client not in clients_to_test:
                continue

            # convert 'all' instances to $client
            def convert(ic): return ic._replace(client=client) if ic.client == 'all' else ic

            fixture = Fixture(client, [convert(InstanceConfig.from_dict(i)) for i in config['instances']])
            fixtures.append(fixture)

        return fixtures

    # if any clients in the fixture are not among those specified in clients_to_test, return no fixtures
    elif any((i['client'] not in clients_to_test for i in config['instances'])):
        return []

    else:
        fixture = Fixture(None, [InstanceConfig.from_dict(i) for i in config['instances']])
        return [fixture]


def setup_fixture(fixture: Fixture):
    for instance in fixture.instances:
        if instance.client not in SUPPORTED_CLIENTS:
            raise ValueError(
                f"can't start instance: client {instance_config.client} not supported yet")

        start_instance(instance)


def teardown_fixture(fixture: Fixture):
    for instance in fixture.instances:
        stop_instance(instance.client)
