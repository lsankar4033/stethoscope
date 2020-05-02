import eth_utils
import subprocess

from lib.types import InstanceConfig


def start_instance(config: InstanceConfig, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL):
    if config.client != 'test':
        raise ValueError('only test clients supported at the moment')

    enr = config.enr

    return subprocess.Popen(
        ['lighthouse', 'bn',
         '--listen-address', enr.ip,
            '--port', str(enr.tcp),
            '--p2p-priv-key', enr.private_key,
            'testnet',
            '--spec', 'minimal',
            '-f', 'file', 'ssz', config.beacon_state_path],
        stdout=stdout,
        stderr=stderr
    )


def start_instances(test_config):
    instance_configs = [InstanceConfig.from_dict(i) for i in test_config['instances']]
    return [start_instance(c) for c in instance_configs]


def stop_instances(instance_processes):
    for p in instance_processes:
        p.terminate()
