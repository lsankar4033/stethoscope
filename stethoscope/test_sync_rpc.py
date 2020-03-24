from pyrum import Rumor

import asyncio
import io
import os
import pytest

from stethoscope.types import Status
from stethoscope.constants import GENESIS_FORK_VERSION, GENESIS_ROOT


# TODO: get this from the lighthouse node I start here
LIGHTHOUSE_ENR = 'enr:-Iu4QECZDNRnrQxHRwRtXDqy5GmWFN1ncBVT0AZHQxSnwO-VA7dealq9eWyCw2G4JNWrWf9qmuAxlmBfQ7Iw8v5AtZ8BgmlkgnY0gmlwhH8AAAGJc2VjcDI1NmsxoQIOcyGUVCsGfZH3VpRKDEKONbxJtDBto6VVj_F_wrtHbYN0Y3CCIyiDdWRwgiMo'


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
    print(f'received status response: {status}')

    await rumor.stop()
    print('stoped rumor')

    assert True
