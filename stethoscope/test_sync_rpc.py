from pyrum import Rumor

import asyncio
import io
import os
import pytest

from stethoscope.clients import LighthouseClient
from stethoscope.constants import GENESIS_FORK_VERSION, GENESIS_ROOT
from stethoscope.types import Status


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
