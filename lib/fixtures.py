import eth_utils
import os
import subprocess

from lib.types import Fixture, InstanceConfig, List


all_clients = [
    'lighthouse',
    'prysm',
    'nimbus',
    'teku',
    'lodestar',
    'nethermind',
    'trinity'
]


def client_supported(client):
    return os.path.exists(f'clients/{client}/start.sh') and os.path.exists(f'clients/{client}/stop.sh')


supported_clients = list(filter(client_supported, all_clients))


def extract_fixtures(config) -> List[Fixture]:
    # turn a yml config into a list of fixtures. if any 'all' in the file, do 1:1 for all alls (rather than all
    # pairwise combos)
    if any((i['client'] == 'all' for i in config['instances'])):
        fixtures = []

        for client in all_clients:
            # convert 'all' instances to $client
            def convert(ic): return ic._replace(client=client) if ic.client == 'all' else ic

            fixture = Fixture(client, [convert(InstanceConfig.from_dict(i)) for i in config['instances']])
            fixtures.append(fixture)

        return fixtures

    else:
        fixture = Fixture(None, [InstanceConfig.from_dict(i) for i in config['instances']])
        return [fixture]


def setup_fixture(fixture: Fixture):
    for instance in fixture.instances:
        start_instance(instance)


def teardown_fixture(fixture: Fixture):
    for instance in fixture.instances:
        stop_instance(instance)


def start_instance(instance_config: InstanceConfig, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL):
    if instance_config.client not in set(supported_clients):
        raise ValueError(
            f"can't start instance: client {instance_config.client} not supported yet")

    start_script = f'clients/{instance_config.client}/start.sh'
    output = subprocess.run(
        # TODO: pass in startup args
        ['sh', start_script],
        stdout=stdout,
        stderr=stderr,
        text=True
    )
    if output.stdout is not None and len(output.stdout) > 0:
        print(output.stdout)


def stop_instance(instance_config: InstanceConfig, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL):
    output = subprocess.run(
        ['sh', 'clients/lighthouse/stop.sh'],
        stdout=stdout,
        stderr=stderr,
        text=True
    )
    if output.stdout is not None and len(output.stdout) > 0:
        print(output.stdout)


def stop_instances(instance_configs):
    stop_script = f'clients/{instance_config.client}/stop.sh'
    for c in instance_configs:
        output = subprocess.run(
            ['sh', stop_script],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )
