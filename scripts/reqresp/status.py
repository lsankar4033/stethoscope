from eth2spec.utils.ssz.ssz_typing import (
    Bytes4, Bytes32, Container, uint64
)
from pyrum import Rumor

import trio


# minimal config
GENESIS_FORK_VERSION = '0x00000001'


class Status(Container):
    version: Bytes4
    finalized_root: Bytes32
    finalized_epoch: uint64
    head_root: Bytes32
    head_slot: uint64


async def test_status(enr, beacon_state_path):
    async with Rumor(cmd='rumor') as rumor:
        print('Testing status')
        await rumor.host.start()

        # NOTE: will fail if ENR isn't available
        peer_id = await rumor.peer.connect(enr).peer_id()

        req = Status(head_slot=0).encode_bytes().hex()
        resp = await rumor.rpc.status.req.raw(peer_id, req, raw=True)
        resp_status = Status.decode_bytes(bytes.fromhex(resp['chunk']['data']))

        # TODO: derive this from beacon_state
        assert resp_status == Status(
            version=GENESIS_FORK_VERSION,
            head_root='0xef64a1b94652cd9070baa4f9c0e8b1ce624bdb071b77b51b1a54b8babb1a5cd2',
        )
        print('Successfully tested status')


async def test_fn(foo):
    print(f'hello! {foo}')


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    req_grp = parser.add_argument_group(title='required')
    req_grp.add_argument('--enr', required=True)
    req_grp.add_argument('--beacon_state_path', required=True)

    args = parser.parse_args()

    trio.run(test_status, args.enr, args.beacon_state_path)
