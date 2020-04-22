from eth2spec.phase0.spec import SignedBeaconBlock
from pyrum import Rumor

import os
import pytest

from stethoscope.client import build_client
from stethoscope.genesis import spec
from stethoscope.reqresp import Status, BlocksByRangeReqV1, BlocksByRangeReqV2


@pytest.fixture(scope='session')
def minimal_client():
    client = build_client('simple_minimal')
    client.start()

    yield client

    client.stop()


# NOTE: trio fixture
@pytest.fixture
async def single_client_rumor(minimal_client):
    async with Rumor(cmd='rumor') as rumor:
        await rumor.host.start()
        await rumor.host.listen(tcp=9001)

        client_id = await rumor.peer.connect(minimal_client.enr()).peer_id()

        yield (rumor, client_id)


# Tests that client started up properly
def test_client_startup(minimal_client):
    import time
    time.sleep(0.5)  # TODO: Do something better here
    assert minimal_client.is_running()


async def test_status_rpc(single_client_rumor):
    rumor, client_id = single_client_rumor

    req = Status(
        version=spec.GENESIS_FORK_VERSION,
        finalized_root='0x0000000000000000000000000000000000000000000000000000000000000000',
        finalized_epoch=0,
        head_root='0x0000000000000000000000000000000000000000000000000000000000000000',
        head_epoch=0
    ).encode_bytes().hex()
    resp = await rumor.rpc.status.req.raw(client_id, req, raw=True)
    resp_status = Status.decode_bytes(bytes.fromhex(resp['chunk']['data']))

    assert resp_status == Status(
        version=spec.GENESIS_FORK_VERSION,
        finalized_root='0x0000000000000000000000000000000000000000000000000000000000000000',
        finalized_epoch=0,
        head_root='0xef64a1b94652cd9070baa4f9c0e8b1ce624bdb071b77b51b1a54b8babb1a5cd2',
        head_epoch=0
    )


# NOTE: may not be supported on clients yet
# async def test_genesis_blocks_by_range_v2(single_client_rumor):
    #rumor, client_id = single_client_rumor

    # req = BlocksByRangeReqV2(
    # start_slot=0,
    # count=1,
    # step=1
    # ).encode_bytes().hex()
    # resp = await rumor.rpc.blocks_by_range_v2.req.raw(client_id, req, raw=True)

    #first_block = SignedBeaconBlock.decode_bytes(bytes.fromhex(resp['chunk']['data']))
    # print(first_block)


# async def test_genesis_blocks_by_range_v1(single_client_rumor):
    #rumor, client_id = single_client_rumor

    # req = BlocksByRangeReqV1(
    # head_block_root='0x0000000000000000000000000000000000000000000000000000000000000000',
    # start_slot=0,
    # count=1,
    # step=1
    # ).encode_bytes().hex()
    # resp = await rumor.rpc.blocks_by_range.req.raw(client_id, req, raw=True)

    #first_block = SignedBeaconBlock.decode_bytes(bytes.fromhex(resp['chunk']['data']))
    # print(first_block)
