import argparse
import sys

from eth2spec.utils.ssz.ssz_typing import Container


def parse_args(*args):
    parser = argparse.ArgumentParser()
    req_grp = parser.add_argument_group(title='required')

    for arg in args:
        req_grp.add_argument(arg, required=True)

    return parser.parse_args()


def compare_containers(expected: Container, actual: Container):
    if expected != actual:
        error_str = ''
        for field in expected.fields():
            if getattr(expected, field) != getattr(actual, field):
                print(
                    f'{field} -- expected {getattr(expected, field)} actual {getattr(actual, field)}',
                    file=sys.stderr
                )


def parse_response(resp):
    if not('chunk' in resp and 'data' in resp['chunk']):
        print(f'received bad response: {resp}', file=sys.stderr)
        return None

    return resp['chunk']['data']
