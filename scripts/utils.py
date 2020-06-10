import argparse


def parse_args(*args):
    parser = argparse.ArgumentParser()
    req_grp = parser.add_argument_group(title='required')

    for arg in args:
        req_grp.add_argument(arg, required=True)

    return parser.parse_args()
