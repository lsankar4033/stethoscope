from eth2spec.utils.ssz.ssz_typing import Container, uint64
from eth2spec.phase0.spec import SignedBeaconBlock, Slot

from pyrum import Rumor

import trio


class BlocksByRangeReq(Container):
    start_slot: Slot
    count: uint64
    step: uint64


async def test_blocks_by_range(enr, beacon_state):
    async with Rumor(cmd='rumor') as rumor:
        print('testing blocks-by-range')
        await rumor.host.start()

        peer_id = await rumor.peer.connect(enr).peer_id()

        req = BlocksByRangeReq(
            count=1,
            step=1
        ).encode_bytes().hex()

        blocks = []
        async for chunk in rumor.rpc.blocks_by_range.req.raw(peer_id, req, raw=True).chunk():
            if chunk['result_code'] == 0:
                block = SignedBeaconBlock.decode_bytes(bytes.fromhex(chunk['data']))
                blocks.append(block)

        # TODO: make test here based on beacon_state
        assert blocks == []

        print("successfully tested blocks-by-range")

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    req_grp = parser.add_argument_group(title='required')
    req_grp.add_argument('--enr', required=True)
    req_grp.add_argument('--beacon_state_path', required=True)

    args = parser.parse_args()

    trio.run(test_blocks_by_range, args.enr, args.beacon_state_path)
