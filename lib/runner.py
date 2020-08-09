import importlib
import os
import subprocess

import trio
from colored import fg

from lib.console import ConsoleWriter
from lib.instance_configs import DEFAULT_ARGS

TESTS_DIR = 'tests'

def all_test_files():
    tests = []
    for root, dirs, files in os.walk(TESTS_DIR):
        # skip files in top-level
        if root == 'tests':
            continue

        tests.extend([f'{root}/{f}' for f in files if f.endswith('.py')])

    return tests

def file_to_module(script):
    return script.replace('/', '.')[0:-3]

def return_code_to_status(return_code):
    if return_code == 0:
        return f"{fg('green')}\u2713{fg('white')}"

    else:
        return f"{fg('red')}\u2717{fg('white')}"

def run_module(module_str, args):
    module = importlib.import_module(module_str)

    if not hasattr(module, 'run'):
        cw.fail(f'module {module} does not have a run method')
        return

    return_code = trio.run(module.run, args)

    print(f'\t{module_str} {return_code_to_status(return_code)}')

def test_matches_filter(test, test_filter):
    return test_filter is None or test == test_filter

def run_all_tests(cw=ConsoleWriter(None, None), test_filter=None):
    for test_file in all_test_files():
        if test_matches_filter(test_file, test_filter):
            cw = cw._replace(test=file_to_module(test_file))

            run_module(file_to_module(test_file), DEFAULT_ARGS)
