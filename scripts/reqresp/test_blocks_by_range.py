from eth2spec.utils.ssz.ssz_typing import Container, uint64
from eth2spec.phase0.spec import SignedBeaconBlock, Slot

from pyrum import Rumor


class BlocksByRangeReq(Container):
    start_slot: Slot
    count: uint64
    step: uint64


async def test_blocks_by_range(enr, genesis):
    async with Rumor(cmd='rumor') as rumor:
        print('Testing blocks-by-range')
        await rumor.host.start()

        peer_id = await rumor.peer.connect(enr).peer_id()

        req = BlocksByRangeReq(
            count=1,
            step=1
        ).encode_bytes().hex()

        blocks = []
        async for chunk in rumor.rpc.blocks_by_range.req.raw(peer_id, req, raw=True).chunk():
            if chunk['result_code'] == 0:
                block = SignedBeaconBlock.decode_bytes(byes.fromhex(chunk['data']))
                blocks.append(block)

        # TODO: make test here based on genesis
        assert blocks == []

        print("Successfully tested blocks-by-range")
