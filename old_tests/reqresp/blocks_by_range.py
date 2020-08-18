from eth2spec.utils.ssz.ssz_typing import Container, uint64
from eth2spec.phase0.spec import BeaconBlock, SignedBeaconBlock, Slot
from pyrum import SubprocessConn, Rumor
from sclients import connect_rumor

from ..utils import *

import trio


class Request(Container):
    start_slot: Slot
    count: uint64
    step: uint64


async def test_blocks_by_range(enr, beacon_state):
    async with SubprocessConn(cmd='rumor bare') as conn:
        async with trio.open_nursery() as nursery:
            rumor = Rumor(conn, nursery)
            peer_id = await connect_rumor(rumor, enr)

            req = Request(
                count=1,
                step=1
            ).encode_bytes().hex()

            blocks = []
            async for chunk in rumor.rpc.blocks_by_range.req.raw(peer_id, req, raw=True, compression='snappy').chunk():
                if chunk['result_code'] == 0:
                    block = SignedBeaconBlock.decode_bytes(bytes.fromhex(chunk['data']))
                    blocks.append(block)

            compare_vals(1, len(blocks), 'num_blocks')
            compare_containers(SignedBeaconBlock(
                message=BeaconBlock(
                    state_root='0x363bcbffb8bcbc8db51bda09cb68a5a3cc7cb2c1b79f8301a3157e37e24c687d')
            ), blocks[0])

            nursery.cancel_scope.cancel()


if __name__ == '__main__':
    args = parse_args('--enr', '--beacon_state_path')
    trio.run(test_blocks_by_range, args.enr, args.beacon_state_path)
