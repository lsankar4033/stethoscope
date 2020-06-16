from eth2spec.utils.ssz.ssz_typing import (
    Bytes4, Bytes32, Container, uint64
)
from pyrum import SubprocessConn, Rumor
from sclients import connect_rumor
import trio

from ..utils import compare_containers, parse_args


class Request(Container):
    version: Bytes4
    finalized_root: Bytes32
    finalized_epoch: uint64
    head_root: Bytes32
    head_slot: uint64


async def test_status(enr, beacon_state_path):
    async with SubprocessConn(cmd='rumor bare') as conn:
        async with trio.open_nursery() as nursery:
            rumor = Rumor(conn, nursery)
            peer_id = await connect_rumor(rumor, enr)

            req = Request(head_slot=0).encode_bytes().hex()
            resp = await rumor.rpc.status.req.raw(peer_id, req, raw=True, compression='snappy')
            resp_status = Request.decode_bytes(bytes.fromhex(resp['chunk']['data']))

            compare_containers(
                Request(
                    version=resp_status.version,
                    finalized_root='0x0000000000000000000000000000000000000000000000000000000000000000',
                    head_root='0xef64a1b94652cd9070baa4f9c0e8b1ce624bdb071b77b51b1a54b8babb1a5cd2',
                ),
                resp_status
            )

            nursery.cancel_scope.cancel()

if __name__ == '__main__':
    args = parse_args('--enr', '--beacon_state_path')
    trio.run(test_status, args.enr, args.beacon_state_path)
