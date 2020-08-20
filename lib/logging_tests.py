import os
from typing import List

from sclients import SUPPORTED_CLIENTS

from lib.beacon_state import BeaconState
from lib.runner import run_module, file_to_module, return_code_to_status
from lib.test_groups import get_test_groups, TestGroup

LOGGING_TESTS_DIR = 'logging_tests'

LOGGING_TEST_FILE_TO_CONFIGS = {
    'logging_tests/test_success.py': [BeaconState.DEFAULT],
    'logging_tests/test_fail.py': [BeaconState.DEFAULT],
}


def get_logging_test_groups() -> List[TestGroup]:
    return get_test_groups(LOGGING_TEST_FILE_TO_CONFIGS, SUPPORTED_CLIENTS, None)


def all_logging_test_files():
    tests = []
    for root, dirs, files in os.walk(LOGGING_TESTS_DIR):
        tests.extend([f'{root}/{f}' for f in files if f.endswith('.py')])

    return tests
