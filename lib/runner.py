import importlib
import os
import subprocess

import trio

from lib.console import ConsoleWriter

TESTS_DIR = 'scripts'

def all_test_files():
    tests = []
    for root, dirs, files in os.walk(TESTS_DIR):
        # skip files in top-level
        if root == 'scripts':
            continue

        tests.extend([f'{root}/{f}' for f in files if f.endswith('.py')])

    return tests

def file_to_module(script):
    return script.replace('/', '.')[0:-3]


# TODO: add args back in
def run_module(module, cw):
    print(f'Running module: {module}')
    #module = importlib.import_module(module)

    #if not hasattr(module, 'run'):
        #cw.fail(f'module {module} does not have a run method')
        #return

    #return_code = trio.run(module.run, args)
    #if return_code == 0:
        #cw.success('SUCCESS')

    #else:
        #cw.fail('FAILED')


def test_matches_filter(test, test_filter):
    return test_filter is None or test == test_filter

def run_all_tests(cw=ConsoleWriter(None, None), test_filter=None):
    for test_file in all_test_files():
        if test_matches_filter(test_file, test_filter):
            cw = cw._replace(test=file_to_module(test_file))

            run_module(file_to_module(test_file), cw)
