import argparse
import os
import yaml

from lib.console import ConsoleWriter
from lib.fixtures import extract_fixtures, setup_fixture, teardown_fixture
from lib.runner import run_test_suite
from lib.types import ENR, InstanceConfig

TESTS_DIR = 'tests'


def run_suite(suite):
    suite_file = f'{TESTS_DIR}/{suite}.yml'
    with open(suite_file, 'r') as f:
        full_config = yaml.load(f, Loader=yaml.Loader)

    cw = ConsoleWriter(suite, None, None)
    fixtures = extract_fixtures(full_config)

    for fixture in fixtures:
        cw = cw._replace(fixture=fixture.name)
        try:
            # TODO: return teardown instructions here
            cw.info('attempting setup_fixture')
            setup_fixture(fixture)
        except ValueError as e:
            cw.info(f'skipping fixture: {e}')
            continue

        try:
            run_test_suite(full_config, cw)

        finally:
            cw.info('attempting teardown_fixture')
            teardown_fixture(fixture)


def run_all_suites():
    for suite_file in os.listdir(TESTS_DIR):
        if suite_file.endswith('.yml'):
            run_suite(suite_file[0:len(suite_file) - 4])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run a single stethoscope test')
    parser.add_argument('-t', '--test', help='run a specific test suite by name')

    args = parser.parse_args()

    if args.test is None:
        run_all_suites()

    else:
        run_suite(args.test)
