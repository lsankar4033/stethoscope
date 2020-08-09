import os

from lib.runner import run_module, file_to_module

LOGGING_TESTS_DIR = 'logging_tests'

def all_logging_test_files():
    tests = []
    for root, dirs, files in os.walk(LOGGING_TESTS_DIR):
        tests.extend([f'{root}/{f}' for f in files if f.endswith('.py')])

    return tests


def run_logging_tests(client):
    # print client, then call run_module for each test. collect all failures and print them at the end
    print(client)
    for file in all_logging_test_files():
        # TODO: collect failure
        run_module(file_to_module(file), {})

    # TODO: print out all failures + logs
