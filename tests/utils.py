import sys
import trio

from eth2spec.utils.ssz.ssz_typing import Container
from pyrum import SubprocessConn, Rumor

def with_rumor(async_run_fn):
    async def wrapped_run_fn(args):
        async with SubprocessConn(cmd='./bin/rumor bare --level=trace') as conn:
            async with trio.open_nursery() as nursery:
                try:
                    rumor = Rumor(conn, nursery)
                    response_code = await async_run_fn(rumor, args)
                    return response_code

                finally:
                    nursery.cancel_scope.cancel()

    return wrapped_run_fn

def parse_chunk_response(resp):
    if not(resp['result_code'] == 0):
        return (None, [f"request error: {resp['msg']}"])

    if 'data' not in resp:
        return (None, [f"request error: 'data' field not in response"])

    return (resp['data'], [])
