import os

from lib.runner import run_module, file_to_module, return_code_to_status

LOGGING_TESTS_DIR = 'logging_tests'

def all_logging_test_files():
    tests = []
    for root, dirs, files in os.walk(LOGGING_TESTS_DIR):
        tests.extend([f'{root}/{f}' for f in files if f.endswith('.py')])

    return tests


def run_logging_tests(client):
    print(client)

    failures = {}
    for file in all_logging_test_files():
        module = file_to_module(file)
        (return_code, logs) = run_module(module, {})

        print(f'\t{module} {return_code_to_status(return_code)}')
        if return_code != 0:
            failures[module] = (return_code, logs)

    if len(failures) > 0:
        for module, (return_code, logs) in failures.items():
            print('')
            print(f'\t{module} {return_code_to_status(return_code)}')

            for log in logs:
                print(f'\t{log}')

        return 1

    return 0
