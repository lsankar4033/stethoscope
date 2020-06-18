#!/usr/bin/env python

import argparse
import os
import yaml
from sclients import SUPPORTED_CLIENTS, stop_instance

from lib.console import ConsoleWriter
from lib.fixtures import extract_fixtures, setup_fixture, teardown_fixture
from lib.runner import run_test_config

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
            run_test_config(full_config, cw, test_to_run)

        finally:
            teardown_fixture(fixture)


def load_suite_config(suite):
    suite_file = f'{SUITES_DIR}/{suite}.yml'
    with open(suite_file, 'r') as f:
        config = yaml.load(f, Loader=yaml.Loader)
    return config


def run_start_fixture(args):
    client = args.client
    suite = args.suite
    cw = ConsoleWriter(suite, None, None)

    config = load_suite_config(suite)
    fixtures = extract_fixtures(config, [client])

    for fixture in fixtures:
        cw = cw._replace(fixture=fixture.name)
        cw.info('setting up fixture')
        setup_fixture(fixture)


def run_stop_fixture(args):
    cw = ConsoleWriter(None, None, None)
    for client in SUPPORTED_CLIENTS:
        cw.info(f'stopping client {client}')
        stop_instance(client)


def run_test(args):
    clients = SUPPORTED_CLIENTS if args.client is None else [args.client]
    suite = args.suite

    reuse_clients = args.reuse
    tests_to_run = args.only

    cw = ConsoleWriter(suite, None, None)

    config = load_suite_config(suite)
    fixtures = extract_fixtures(config, clients)
    for fixture in fixtures:
        cw = cw._replace(fixture=fixture.name)

        if reuse_clients:
            run_test_config(config, cw, tests_to_run)

        else:
            try:
                cw.info('setting up fixture')
                setup_fixture(fixture)

            except ValueError as e:
                cw.info(f'skipping fixture: {e}')
                continue

            try:
                run_test_config(full_config, cw, test_to_run)

            finally:
                cw.info('tearing down fixture')
                teardown_fixture(fixture)


if __name__ == '__main__':
    steth = argparse.ArgumentParser(description='Stethoscope tool for running multi-client Eth2 scenarios')
    steth_sub = steth.add_subparsers()

    fixture = steth_sub.add_parser('fixture', help='Manage fixtures of client instances')
    fixture_sub = fixture.add_subparsers()

    start = fixture_sub.add_parser('start')
    start.add_argument('suite', help='suite file to parse fixtures from')
    start.add_argument(
        'client', help=f'client to start. can only start 1 at a time until dynamic ENRs implemented. possible values: {SUPPORTED_CLIENTS}')
    start.set_defaults(func=run_start_fixture)

    stop = fixture_sub.add_parser('stop')
    stop.set_defaults(func=run_stop_fixture)

    test = steth_sub.add_parser('test', help='Run stethoscope unit tests')
    test.add_argument('-c', '--client',
                      help='run test(s) for a specific client. possible values: {SUPPORTED_CLIENTS}')
    test.add_argument('-o', '--only', help='run specific tests by name', nargs='*')
    test.add_argument('-r', '--reuse', default=False, action='store_true', help='reuse running fixtures')
    test.add_argument('suite', help='suite file to run')
    test.set_defaults(func=run_test)

    args = steth.parse_args()
    args.func(args)
