import subprocess

from lib.console import ConsoleWriter


def script_to_module(script):
    return script.replace('/', '.')[0:-3]


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


def script_to_test(script):
    remove_prefix_suffix = script[8:len(script) - 3]
    return remove_prefix_suffix.replace('/', '.')


def run_test_config(test_config, cw=ConsoleWriter(None, None, None), tests_to_run=[]):
    tests = test_config['test_suite']

    for test in tests:
        if len(tests_to_run) == 0 or test['name'] in tests_to_run:
            script = test['script']
            args = test['args']

            cw = cw._replace(test=script_to_test(script))

            run_script(script, args, cw)
