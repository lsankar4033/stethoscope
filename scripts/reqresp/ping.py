import sys

import trio
from eth2spec.utils.ssz.ssz_typing import uint64
from pyrum import SubprocessConn, Rumor
from sclients import connect_rumor

from ..utils import *


async def test_ping(enr):
    async with SubprocessConn(cmd='rumor bare') as conn:
        async with trio.open_nursery() as nursery:
            rumor = Rumor(conn, nursery)
            peer_id = await connect_rumor(rumor, enr)

            for i in range(5):
                req = uint64(i).encode_bytes().hex()
                resp = await rumor.rpc.ping.req.raw(peer_id, req, raw=True, compression='snappy')
                resp_data = parse_response(resp)

                pong = uint64.decode_bytes(bytes.fromhex(resp_data))

                if not isinstance(pong, int) or pong < 0:
                    print(
                        f'ping -- invalid ping response: {pong}',
                        file=sys.stderr
                    )

            nursery.cancel_scope.cancel()

if __name__ == '__main__':
    args = parse_args('--enr')
    trio.run(test_ping, args.enr)
