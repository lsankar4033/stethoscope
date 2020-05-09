from eth2spec.utils.ssz.ssz_typing import uint64, Bitvector, Container
from pyrum import SubprocessConn, Rumor
from ..utils import parse_args, connect_rumor

import trio


class Metadata(Container):
    seq_number: uint64
    attnets: Bitvector[64]


async def test_metadata(enr):
    async with SubprocessConn(cmd='rumor bare') as conn:
        async with trio.open_nursery() as nursery:
            rumor = Rumor(conn, nursery)
            peer_id = await connect_rumor(rumor, enr)

            resp = await rumor.rpc.metadata.req.raw(peer_id, '', raw=True)
            metadata = Metadata.decode_bytes(bytes.fromhex(resp['chunk']['data']))

            assert metadata == Metadata(seq_number=1), f'actual metadata: {metadata}'

            nursery.cancel_scope.cancel()

if __name__ == '__main__':
    args = parse_args('--enr')
    trio.run(test_metadata, args.enr)
