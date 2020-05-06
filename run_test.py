import argparse
import yaml

from lib.client_instances import start_instances, stop_instances
from lib.test_runner import run_test_config
from lib.types import ENR, InstanceConfig


def run_test(test):
    with open(test, 'r') as f:
        test_config = yaml.load(f, Loader=yaml.Loader)

    # TODO: if client is 'all' for any instances, do this for *all* clients
    print("Only starting lighthouse instances because that's the only client startup script we have right now")
    instance_configs = start_instances(test_config)

    try:
        run_test_config(test_config)

    finally:
        stop_instances(instance_configs)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run a single stethoscope test')
    parser.add_argument('test')

    args = parser.parse_args()

    run_test(args.test)
