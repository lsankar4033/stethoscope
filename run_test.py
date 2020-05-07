import argparse
import yaml

from lib.fixtures import extract_fixtures, setup_fixture, teardown_fixture
from lib.runner import run_test_suite
from lib.types import ENR, InstanceConfig


def run_test(test):
    with open(test, 'r') as f:
        full_config = yaml.load(f, Loader=yaml.Loader)

    fixtures = extract_fixtures(full_config)

    for fixture in fixtures:
        try:
            # TODO: return teardown instructions here
            setup_fixture(fixture)
        except ValueError as e:
            print(f'skipping fixture: {e}')
            continue

        try:
            # TODO: make this better
            run_test_suite(full_config)

        finally:
            teardown_fixture(fixture)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run a single stethoscope test')
    parser.add_argument('test')

    args = parser.parse_args()

    run_test(args.test)
