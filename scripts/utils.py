import argparse
import sys
import trio

from eth2spec.utils.ssz.ssz_typing import Container
from pyrum import SubprocessConn, Rumor

from lib.console import ConsoleWriter

def with_rumor(async_run_fn):
    async def wrapped_run_fn(args):
        async with SubprocessConn(cmd='rumor bare --level=trace') as conn:
            async with trio.open_nursery() as nursery:
                try:
                    rumor = Rumor(conn, nursery)
                    response_code = await async_run_fn(rumor, args)
                    return response_code

                finally:
                    nursery.cancel_scope.cancel()

    return wrapped_run_fn


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
            compare_vals(getattr(expected, field), getattr(actual, field), field)


def compare_vals(expected, actual, name):
    if expected != actual:
        print(
            f'{name} -- expected {expected} actual {actual}',
            file=sys.stderr
        )


def parse_response(resp):
    if not('chunk' in resp and 'data' in resp['chunk']):
        print(f'received bad response: {resp}', file=sys.stderr)
        return None

    return resp['chunk']['data']
