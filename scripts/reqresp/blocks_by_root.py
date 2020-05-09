from eth2spec.utils.ssz.ssz_typing import uint64, List
from eth2spec.phase0.spec import BeaconBlock, Root, SignedBeaconBlock
from pyrum import SubprocessConn, Rumor

from ..utils import connect_rumor, parse_args

import trio


async def test_blocks_by_root(enr, beacon_state):
    async with SubprocessConn(cmd='rumor bare') as conn:
        async with trio.open_nursery() as nursery:
            rumor = Rumor(conn, nursery)
            peer_id = await connect_rumor(rumor, enr)

            req = List[Root, 64](
                ['ef64a1b94652cd9070baa4f9c0e8b1ce624bdb071b77b51b1a54b8babb1a5cd2']).encode_bytes().hex()
            blocks = []
            async for chunk in rumor.rpc.blocks_by_root.req.raw(peer_id, req, raw=True).chunk():
                if chunk['result_code'] == 0:
                    block = SignedBeaconBlock.decode_bytes(bytes.fromhex(chunk['data']))
                    blocks.append(block)

            assert blocks == [SignedBeaconBlock(
                message=BeaconBlock(
                    state_root='0x363bcbffb8bcbc8db51bda09cb68a5a3cc7cb2c1b79f8301a3157e37e24c687d')
            )], f'actual blocks: {blocks}'

            nursery.cancel_scope.cancel()


if __name__ == '__main__':
    args = parse_args('--enr', '--beacon_state_path')
    trio.run(test_blocks_by_root, args.enr, args.beacon_state_path)
