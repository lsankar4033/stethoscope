import importlib
import os
import subprocess

import trio
from colors import color

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
        return color('\u2713', fg='green')

    else:
        return color('\u2717', fg='red')


def run_module(module_str, args):
    module = importlib.import_module(module_str)

    if not hasattr(module, 'run'):
        print(f'\t{module} does not have a run method')
        return

    return_code, logs = trio.run(module.run, args)

    return (return_code, logs)


def file_matches_filter(file, file_filter):
    return file_filter is None or file == file_filter


def run_test_files(client, files, args):
    failures = {}
    for file in files:
        module = file_to_module(file)
        (return_code, logs) = run_module(module, {**args, 'client': client})

        print(f'\t{module} {return_code_to_status(return_code)}')
        if return_code != 0:
            failures[module] = (return_code, logs)

    # TODO: report all errors *at the end* of test run
    if len(failures) > 0:
        print('')
        print('--failures--')
        for module, (return_code, logs) in failures.items():
            print(f'\t{module} {return_code_to_status(return_code)}')

            for log in logs:
                print(f'\t\t{log}')

            print('')

        return 1

    return 0
