import importlib
import subprocess

import trio

from lib.console import ConsoleWriter


def script_to_module(script):
    return script.replace('/', '.')[0:-3]


def script_to_test(script):
    remove_prefix_suffix = script[8:len(script) - 3]
    return remove_prefix_suffix.replace('/', '.')


def run_script(script, args, cw):
    script_list = ['python3', '-m', script_to_module(script)]
    arg_list = [item for sublist in [['--' + k, v] for k, v in args.items()] for item in sublist]

    output = subprocess.run(
        script_list + arg_list,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    if len(output.stderr) > 0:
        cw.fail('FAILED')
        cw.info(output.stderr)

    else:
        cw.success('SUCCESS')


def run_module(module, args, cw):
    module = importlib.import_module(module)

    if not hasattr(module, 'run'):
        cw.fail(f'module {module} does not have a run method')
        return

    return_code, msgs = trio.run(module.run, args)
    if return_code == 0:
        cw.success('SUCCESS')

    else:
        cw.fail('FAILED')
        for msg in msgs:
            cw.info(msg)


def test_matches_filter(test, test_filter):
    return test_filter is None or test == test_filter or test.startswith(test_filter)


def run_test_config(test_config, cw=ConsoleWriter(None, None, None), test_filter=None):
    tests = test_config['test_suite']

    for test in tests:
        if test_matches_filter(test['name'], test_filter):
            script = test['script']
            args = test['args']

            cw = cw._replace(test=script_to_test(script))

            # NOTE: special casing this single test for the time being. This should be the normal case going
            # forward
            if test['name'] == 'dv5.single-node':
                run_module(script_to_module(script), args, cw)

            else:
                run_script(script, args, cw)
