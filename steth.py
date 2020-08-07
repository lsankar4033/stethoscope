#!/usr/bin/env python

import argparse
import os
import yaml
from sclients import SUPPORTED_CLIENTS, stop_instance

from lib.console import ConsoleWriter
from lib.fixtures import extract_fixtures, setup_fixture, teardown_fixture
from lib.runner import run_all_tests


def run_start_fixture(args):
    client = args.client
    cw = ConsoleWriter(None, None)

    fixtures = extract_fixtures([client])

    for fixture in fixtures:
        cw = cw._replace(fixture=fixture.name)
        cw.info('setting up fixture')
        setup_fixture(fixture)


def run_stop_fixture(args):
    cw = ConsoleWriter(None, None)
    for client in SUPPORTED_CLIENTS:
        cw.info(f'stopping client {client}')
        stop_instance(client)


def run_test(args):
    clients = SUPPORTED_CLIENTS if args.client is None else [args.client]

    reuse_clients = args.reuse
    test_filter = args.only

    cw = ConsoleWriter(None, None)

    fixtures = extract_fixtures(clients)
    for fixture in fixtures:
        cw = cw._replace(fixture=fixture.name)

        if reuse_clients:
            run_all_tests(cw, test_filter)

        else:
            try:
                cw.info('setting up fixture')
                setup_fixture(fixture)

            except ValueError as e:
                cw.info(f'skipping fixture: {e}')
                continue

            try:
                run_all_tests(cw, test_filter)

            finally:
                cw.info('tearing down fixture')
                teardown_fixture(fixture)


def run_logging_test(args):
    for client in SUPPORTED_CLIENTS:
        print(f'Testing client {client}')


if __name__ == '__main__':
    steth = argparse.ArgumentParser(description='Stethoscope tool for running multi-client Eth2 scenarios')
    steth_sub = steth.add_subparsers()

    fixture = steth_sub.add_parser('fixture', help='Manage fixtures of client instances')
    fixture_sub = fixture.add_subparsers()

    start = fixture_sub.add_parser('start')
    start.add_argument(
        'client', help=f'client to start. can only start 1 at a time until dynamic ENRs implemented. possible values: {SUPPORTED_CLIENTS}')
    start.set_defaults(func=run_start_fixture)

    stop = fixture_sub.add_parser('stop')
    stop.set_defaults(func=run_stop_fixture)

    test = steth_sub.add_parser('test', help='Run stethoscope unit tests')
    test.add_argument('-c', '--client',
                      help='run test(s) for a specific client. possible values: {SUPPORTED_CLIENTS}')
    test.add_argument('-o', '--only', help='run specific tests by name')
    test.add_argument('-r', '--reuse', default=False, action='store_true', help='reuse running fixtures')
    test.set_defaults(func=run_test)

    test = steth_sub.add_parser('logging_test', help='Display example logs from ./steth.py test. Useful for testing CI integration')
    test.set_defaults(func=run_logging_test)

    args = steth.parse_args()
    args.func(args)
