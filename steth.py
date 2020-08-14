#!/usr/bin/env python

import argparse
import os
import yaml
from sclients import SUPPORTED_CLIENTS, stop_instance

from lib.fixtures import extract_fixtures, setup_fixture, teardown_fixture
from lib.instance_configs import DEFAULT_ARGS
from lib.runner import run_test_files, all_test_files, file_matches_filter
from lib.logging_tests import all_logging_test_files


def run_start_fixture_cmd(args):
    client = args.client

    fixtures = extract_fixtures([client])

    for fixture in fixtures:
        setup_fixture(fixture)


def run_stop_fixture_cmd(args):
    for client in SUPPORTED_CLIENTS:
        stop_instance(client)


def run_test_cmd(args):
    clients = SUPPORTED_CLIENTS if args.client is None else [args.client]

    reuse_clients = args.reuse
    file_filter = args.only

    test_files = [file for file in all_test_files() if file_matches_filter(file, file_filter)]
    fixtures = extract_fixtures(clients)
    failed = False
    for fixture in fixtures:
        if not reuse_clients:
            setup_fixture(fixture)

        try:
            return_code = run_test_files(fixture.name, test_files, DEFAULT_ARGS)
            if return_code != 0:
                failed = True

        except Exception as e:
            print(f'Exception while running tests: {e}')
            failed = True

        finally:
            if not reuse_clients:
                teardown_fixture(fixture)
    if failed:
        exit(1)


def run_logging_test(args):
    test_files = all_logging_test_files()

    failed = False
    for client in SUPPORTED_CLIENTS:
        return_code= run_test_files(client, test_files, {})
        if return_code != 0:
            failed = True

    if failed:
        exit(1)

if __name__ == '__main__':
    steth = argparse.ArgumentParser(description='Stethoscope tool for running multi-client Eth2 scenarios')
    steth_sub = steth.add_subparsers()

    fixture = steth_sub.add_parser('fixture', help='Manage fixtures of client instances')
    fixture_sub = fixture.add_subparsers()

    start = fixture_sub.add_parser('start')
    start.add_argument(
        'client', help=f'client to start. can only start 1 at a time until dynamic ENRs implemented. possible values: {SUPPORTED_CLIENTS}')
    start.set_defaults(func=run_start_fixture_cmd)

    stop = fixture_sub.add_parser('stop')
    stop.set_defaults(func=run_stop_fixture_cmd)

    test = steth_sub.add_parser('test', help='Run stethoscope unit tests')
    test.add_argument('-c', '--client',
                      help=f'run test(s) for a specific client. possible values: {SUPPORTED_CLIENTS}')
    test.add_argument('-o', '--only', help='run specific tests by name')
    test.add_argument('-r', '--reuse', default=False, action='store_true', help='reuse running fixtures')
    test.set_defaults(func=run_test_cmd)

    test = steth_sub.add_parser('logging_test', help='Display example logs from ./steth.py test. Useful for testing CI integration')
    test.set_defaults(func=run_logging_test)

    args = steth.parse_args()
    args.func(args)
