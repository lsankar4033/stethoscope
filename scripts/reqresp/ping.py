from eth2spec.utils.ssz.ssz_typing import uint64
from pyrum import SubprocessConn, Rumor
from ..utils import parse_args, connect_rumor

import trio


async def test_ping(enr):
    async with SubprocessConn(cmd='rumor bare') as conn:
        async with trio.open_nursery() as nursery:
            rumor = Rumor(conn, nursery)
            peer_id = await connect_rumor(rumor, enr)

            for i in range(5):
                req = uint64(i).encode_bytes().hex()
                resp = await rumor.rpc.ping.req.raw(peer_id, req, raw=True)
                pong = uint64.decode_bytes(bytes.fromhex(resp['chunk']['data']))

                assert pong == 1, f'actual ping response: {pong}'

            nursery.cancel_scope.cancel()

if __name__ == '__main__':
    args = parse_args('--enr')
    trio.run(test_ping, args.enr)
