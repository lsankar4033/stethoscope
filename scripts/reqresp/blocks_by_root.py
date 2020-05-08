from eth2spec.utils.ssz.ssz_typing import Container, uint64
from eth2spec.phase0.spec import Root

from typing import List

from ..utils import connect_rumor


class Request(Container):
    roots: List[Root]


async def test_blocks_by_root(enr, beacon_state):
    async with SubprocessConn(cmd='rumor bare') as conn:
        async with trio.open_nursery() as nursery:
            rumor = Rumor(conn, nursery)
            peer_id = await connect_rumor(rumor, enr)

            req = Request(['0xef64a1b94652cd9070baa4f9c0e8b1ce624bdb071b77b51b1a54b8babb1a5cd2']
                          ).encode_bytes.hex()
            resp = await rumor.rpc.blocks_by_root.req.raw(peer_id, req, raw=True)

            # TODO!

            nursery.cancel_scope.cancel()


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    req_grp = parser.add_argument_group(title='required')
    req_grp.add_argument('--enr', required=True)
    req_grp.add_argument('--beacon_state_path', required=True)

    args = parser.parse_args()

    trio.run(test_blocks_by_root, args.enr, args.beacon_state_path)
