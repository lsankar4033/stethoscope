import argparse
import os
import yaml

from lib.console import ConsoleWriter
from lib.fixtures import all_clients, extract_fixtures, setup_fixture, teardown_fixture
from lib.runner import run_test_suite

SUITES_DIR = 'suites'


def run_suite(suite, clients):
    suite_file = f'{SUITES_DIR}/{suite}.yml'
    with open(suite_file, 'r') as f:
        full_config = yaml.load(f, Loader=yaml.Loader)

    cw = ConsoleWriter(suite, None, None)
    fixtures = extract_fixtures(full_config, clients)

    for fixture in fixtures:
        cw = cw._replace(fixture=fixture.name)
        try:
            # TODO: return teardown instructions here
            setup_fixture(fixture)
            cw.info('setup fixture')
        except ValueError as e:
            cw.info(f'skipping fixture: {e}')
            continue

        try:
            run_test_suite(full_config, cw)

        finally:
            teardown_fixture(fixture)


def run_all_suites(clients):
    for suite_file in os.listdir(SUITES_DIR):
        if suite_file.endswith('.yml'):
            run_suite(suite_file[0:len(suite_file) - 4], clients)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run a single stethoscope test')
    parser.add_argument('-t', '--test', help='run a specific test suite by name')
    parser.add_argument(
        '-c', '--client', help=f'run test(s) for a specific client. possible values: {all_clients}')

    args = parser.parse_args()
    clients = all_clients if args.client is None else [args.client]

    if args.test is None:
        run_all_suites(clients)

    else:
        run_suite(args.test, clients)
