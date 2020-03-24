from pyrum import Rumor
from remerkleable.complex import Container
from remerkleable.byte_arrays import Bytes32, Bytes4
from remerkleable.basic import uint64

import asyncio
import io
import os
import pytest

import stethoscope.fast_spec as spec


class Status(Container):
    version: Bytes4
    finalized_root: Bytes32
    finalized_epoch: uint64
    head_root: Bytes32
    head_slot: uint64


def load_state(filepath: str) -> spec.BeaconState:
    state_size = os.stat(filepath).st_size
    with io.open(filepath, 'br') as f:
        return spec.BeaconState.deserialize(f, state_size)


# TODO: get this from the lighthouse node I start here
LIGHTHOUSE_ENR = 'enr:-Iu4QM7ZznpGrhDZm8C_nJ8jwGtwyd8cH80oH-Icy8cmvloMZGqjZ514KsJAR_uT95DkB_CbFi_EGDVXdZ9ZK8d2LPEBgmlkgnY0gmlwhH8AAAGJc2VjcDI1NmsxoQOK4c3Dmkka6pnmgK10RkznxLZcELEmXnNjH6z-Q8z8I4N0Y3CCIyiDdWRwgiMo'

# TODO: what should this actually be?
GENESIS_FORK_VERSION = spec.Version('0x00000000')


# TODO: put this in a test sync rpc fixture or smth
@pytest.mark.asyncio
async def test_status_reqresp(event_loop):
    rumor = Rumor()
    await rumor.start(cmd='./bin/rumor')
    print('started rumor')

    l_actor = rumor.actor('lighthouse')
    await l_actor.host.start().ok
    await l_actor.host.listen(tcp=9000).ok
    print('started l_actor')

    peer_id = await l_actor.peer.connect(LIGHTHOUSE_ENR).peer_id()
    print(f'connected to lighthouse peer: {peer_id}')

    # TODO: initialize state with specific values
    state = load_state('./genesis.ssz')
    genesis_root = state.hash_tree_root()

    l_status = Status(
        version=GENESIS_FORK_VERSION,
        finalized_root=genesis_root,
        finalized_epoch=0,
        head_root=genesis_root,
        head_epoch=0,
    )
    l_status_resp = await l_actor.rpc.status.req.raw(peer_id, l_status.encode_bytes().hex(), raw=True).ok
    assert l_status_resp['chunk']['result_code'] == 0
    status = Status.decode_bytes(bytes.fromhex(l_status_resp['chunk']['data']))
    print(f'received status response: {status}')

    await rumor.stop()
    print('stoped rumor')

    assert True
