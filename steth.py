#!/usr/bin/env python

import argparse
import os
import yaml
from sclients import SUPPORTED_CLIENTS, start_instance, stop_instance

from lib.instance_configs import DEFAULT_ARGS
from lib.runner import run_test_files
from lib.logging_tests import get_logging_test_groups
from lib.test_groups import TEST_FILE_TO_CONFIGS, get_test_groups


def run_test_cmd(args):
    clients = SUPPORTED_CLIENTS if args.client is None else [args.client]

    file_filter = args.only

    test_groups = get_test_groups(TEST_FILE_TO_CONFIGS, clients, file_filter)

    failed = False
    for test_group in test_groups:
        print(test_group)

        start_instance(test_group.instance_config)

        try:
            # TODO: replace test_files + args with instance_config
            return_code = run_test_files(test_group.instance_config.client,
                                         test_group.test_files,
                                         {
                                             'beacon_state_path': test_group.instance_config.beacon_state_path,
                                             'enr': test_group.instance_config.enr
                                         })
            if return_code != 0:
                failed = True

        except Exception as e:
            print(f'Exception while running tests: {e}')
            failed = True

        finally:
            stop_instance(test_group.instance_config.client)

    if failed:
        exit(1)


def run_logging_test(args):
    test_groups = get_logging_test_groups()

    failed = False
    for test_group in test_groups:
        print(test_group)

        return_code = run_test_files(test_group.instance_config.client, test_group.test_files, {})
        if return_code != 0:
            failed = True

    if failed:
        exit(1)


if __name__ == '__main__':
    steth = argparse.ArgumentParser(description='Stethoscope tool for running multi-client Eth2 scenarios')
    steth_sub = steth.add_subparsers()

    test = steth_sub.add_parser('test', help='Run stethoscope unit tests')
    test.add_argument('-c', '--client',
                      help=f'run test(s) for a specific client. possible values: {SUPPORTED_CLIENTS}')
    test.add_argument('-o', '--only', help='run specific tests by name')
    test.set_defaults(func=run_test_cmd)

    test = steth_sub.add_parser(
        'logging_test', help='Display example logs from ./steth.py test. Useful for testing CI integration')
    test.set_defaults(func=run_logging_test)

    args = steth.parse_args()
    args.func(args)
