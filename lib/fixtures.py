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


def extract_fixtures(config, clients_to_test=all_clients) -> List[Fixture]:
    # turn a yml config into a list of fixtures. if any 'all' in the file, do 1:1 for every one (rather than all
    # pairwise combos)
    if any((i['client'] == 'all' for i in config['instances'])):
        fixtures = []

        for client in all_clients:
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
        start_instance(instance)


def teardown_fixture(fixture: Fixture):
    for instance in fixture.instances:
        stop_instance(instance)


def start_arg_list(config: InstanceConfig):
    return [
        f'--tcp={config.enr.tcp}',
        f'--udp={config.enr.udp}',
        f'--ip={config.enr.ip}',
        f'--private-key={config.enr.private_key}',
        f'--beacon-state-path={config.beacon_state_path}',
    ]


def start_instance(instance_config: InstanceConfig, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL):
    if instance_config.client not in set(supported_clients):
        raise ValueError(
            f"can't start instance: client {instance_config.client} not supported yet")

    start_script = f'clients/{instance_config.client}/start.sh'
    output = subprocess.run(
        ['sh', start_script] + start_arg_list(instance_config),
        stdout=stdout,
        stderr=stderr,
        text=True
    )
    if output.stdout is not None and len(output.stdout) > 0:
        print(output.stdout)


def stop_instance(instance_config: InstanceConfig, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL):
    output = subprocess.run(
        ['sh', f'clients/{instance_config.client}/stop.sh'],
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
