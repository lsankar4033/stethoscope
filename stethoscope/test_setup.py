from pyrum import Rumor
from remerkleable.complex import Container
from remerkleable.byte_arrays import Bytes32, Bytes4
from remerkleable.basic import uint64

import asyncio
import pytest


class Status(Container):
    version: Bytes4
    finalized_root: Bytes32
    finalized_epoch: uint64
    head_root: Bytes32
    head_slot: uint64


# TODO: Get this dynamically! Or even better, from the lighthouse node I start *here*.
LIGHTHOUSE_ENR = 'enr:-Iu4QM7ZznpGrhDZm8C_nJ8jwGtwyd8cH80oH-Icy8cmvloMZGqjZ514KsJAR_uT95DkB_CbFi_EGDVXdZ9ZK8d2LPEBgmlkgnY0gmlwhH8AAAGJc2VjcDI1NmsxoQOK4c3Dmkka6pnmgK10RkznxLZcELEmXnNjH6z-Q8z8I4N0Y3CCIyiDdWRwgiMo'


@pytest.mark.asyncio
async def test_local_lighthouse(event_loop):
    rumor = Rumor()
    await rumor.start(cmd='./bin/rumor')
    print('started rumor')

    l_actor = rumor.actor('lighthouse')
    await l_actor.host.start().ok
    await l_actor.host.listen(tcp=9000).ok
    print('started l_actor')

    peer_id = await l_actor.peer.connect(LIGHTHOUSE_ENR).peer_id()
    print(f'connected to lighthouse peer: {peer_id}')

    l_status = Status(
            version=spec.GENESIS_FORK_VERSION,
            finalized_root=genesis_root,
            finalized_epoch=0,
            head_root=genesis_root,
            head_epoch=0,
            )

    await l_actor.rpc.status.req.raw(peer_id,

    await rumor.stop()
    print('stoped rumor')

    assert True
