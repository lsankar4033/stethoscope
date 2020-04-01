from eth2spec.test.helpers.deposits import prepare_genesis_deposits
from eth2spec.utils.ssz.ssz_typing import (
    Bytes4, Bytes32, Container, uint64
)
from eth2spec.phase0.spec import initialize_beacon_state_from_eth1

from eth2spec.utils.ssz.ssz_impl import hash_tree_root

from pyrum import Rumor
from hashlib import sha256

import asyncio
import io
import os
import pytest

import stethoscope.minimal_spec as spec

from stethoscope.clients import LighthouseClient


def build_genesis_state():
    # NOTE: taken from pyspec
    eth1_block_hash = b'\x12' * 32
    eth1_timestamp = spec.MIN_GENESIS_TIME

    deposits, deposit_root, _ = prepare_genesis_deposits(
        spec, spec.MIN_GENESIS_ACTIVE_VALIDATOR_COUNT, spec.MAX_EFFECTIVE_BALANCE, signed=True)

    state = initialize_beacon_state_from_eth1(eth1_block_hash, eth1_timestamp, deposits)

    return state

# TODO: move to reqresp file or something


class Status(Container):
    version: Bytes4
    finalized_root: Bytes32
    finalized_epoch: uint64
    head_root: Bytes32
    head_slot: uint64


# TODO: might want more control here in the future
GENESIS_ROOT = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'


# TODO: put this in a test sync rpc fixture or smth
@pytest.mark.asyncio
async def test_status_reqresp(event_loop):

    lighthouse = LighthouseClient()
    await lighthouse.start()
    print('started lighthouse client')

    rumor = Rumor()
    await rumor.start(cmd='./bin/rumor')
    print('started rumor')

    l_actor = rumor.actor('lighthouse')
    await l_actor.host.start().ok
    await l_actor.host.listen(tcp=9000).ok
    print('started l_actor')

    peer_id = await l_actor.peer.connect(lighthouse.enr()).peer_id()
    print(f'connected to lighthouse peer: {peer_id}')

    l_status = Status(
        version=GENESIS_FORK_VERSION,
        finalized_root=GENESIS_ROOT,
        finalized_epoch=0,
        head_root=GENESIS_ROOT,
        head_epoch=0,
    )
    l_status_resp = await l_actor.rpc.status.req.raw(peer_id, l_status.encode_bytes().hex(), raw=True).ok
    assert l_status_resp['chunk']['result_code'] == 0
    status = Status.decode_bytes(bytes.fromhex(l_status_resp['chunk']['data']))

    # TODO: test values
    print(f'received status response: {status}')

    await rumor.stop()
    await lighthouse.stop()
    print('stoped rumor')
