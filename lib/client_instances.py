import eth_utils
import subprocess

from lib.types import InstanceConfig


def start_instance(config: InstanceConfig, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL):
    # TODO: actually check client type
    output = subprocess.run(
        ['sh', 'clients/lighthouse/start.sh'],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )
    if len(output.stdout) > 0:
        print(output.stdout)

    # NOTE: will need to return args (i.e. container name) identifying this instance in the future
    return config


def start_instances(test_config):
    instance_configs = [InstanceConfig.from_dict(i) for i in test_config['instances']]
    return [start_instance(c) for c in instance_configs]


def stop_instances(instance_configs):
    for c in instance_configs:
        output = subprocess.run(
            ['sh', 'clients/lighthouse/stop.sh'],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )
