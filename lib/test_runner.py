import subprocess


def run_script(script, args):
    script_list = ['python', script]
    arg_list = [item for sublist in [['--' + k, v] for k, v in args.items()] for item in sublist]

    output = subprocess.run(
        script_list + arg_list,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )

    if len(output.stdout) > 0:
        print(output.stdout)


def run_test_config(test_config):
    tests = test_config['test_cases']

    for test in tests:
        script = test['script']
        args = test['args']
        run_script(script, args)
