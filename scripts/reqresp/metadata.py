from eth2spec.utils.ssz.ssz_typing import uint64, Bitvector, Container
from pyrum import SubprocessConn, Rumor
from sclients import connect_rumor

from ..utils import *

import trio


class Metadata(Container):
    seq_number: uint64
    attnets: Bitvector[64]


async def test_metadata(enr):
    async with SubprocessConn(cmd='rumor bare') as conn:
        async with trio.open_nursery() as nursery:
            rumor = Rumor(conn, nursery)
            peer_id = await connect_rumor(rumor, enr)

            resp = await rumor.rpc.metadata.req.raw(peer_id, '', raw=True, compression='snappy')
            resp_data = parse_response(resp)

            if resp_data is not None:
                resp_metadata = Metadata.decode_bytes(bytes.fromhex(resp_data))

                compare_containers(
                    Metadata(seq_number=resp_metadata.seq_number),
                    resp_metadata
                )

            nursery.cancel_scope.cancel()

if __name__ == '__main__':
    args = parse_args('--enr')
    trio.run(test_metadata, args.enr)
