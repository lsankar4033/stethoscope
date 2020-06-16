import argparse
import os
import yaml
from sclients import SUPPORTED_CLIENTS

from lib.console import ConsoleWriter
from lib.fixtures import extract_fixtures, setup_fixture, teardown_fixture
from lib.runner import run_test_suite

SUITES_DIR = 'suites'


def run_suite(suite, clients, test_to_run=None):
    # tests_to_run = None means we run all of em
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
            run_test_suite(full_config, cw, test_to_run)

        finally:
            teardown_fixture(fixture)


def run_all_suites(clients):
    for suite_file in os.listdir(SUITES_DIR):
        if suite_file.endswith('.yml'):
            run_suite(suite_file[0:len(suite_file) - 4], clients)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run single-client tests')
    parser.add_argument('-s', '--suite', help='run a specific suite by name')
    parser.add_argument(
        '-t', '--test', help='run a specific test by name. --suite must also be specified for this option to be honored')
    parser.add_argument(
        '-c', '--client', help=f'run test(s) for a specific client. possible values: {SUPPORTED_CLIENTS}')

    args = parser.parse_args()
    clients = SUPPORTED_CLIENTS if args.client is None else [args.client]

    if args.suite is None:
        run_all_suites(clients)

    else:
        run_suite(args.suite, clients, args.test)
