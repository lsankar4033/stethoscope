from pyrum import Rumor

import os
import pytest
import trio

from stethoscope.clients import build_client
from stethoscope.genesis_state import write_genesis_state


GENESIS_PATH = 'ssz/genesis.ssz'


# TODO: add a flag to re-use genesis dir if exists (i.e. for local runs)
@pytest.fixture(scope='session')
def genesis_path(request):
    print(f'writing new genesis file at {GENESIS_PATH}')

    # NOTE: temporary check while testing locally
    if not os.path.isfile(GENESIS_PATH):
        write_genesis_state(GENESIS_PATH)

    yield GENESIS_PATH

    # NOTE: temporarily disabled while testing locally
    #print(f'cleaning up genesis file at {GENESIS_PATH}')
    # os.remove(GENESIS_PATH)

# NOTE: this isn't the right abstraction when we consider multiple genesis files and more complicated (i.e.
# write tests)
@pytest.fixture(scope='session', params=['lighthouse'])
def single_client(request, genesis_path):
    client = build_client(request.param, genesis_path)

    print(f'starting client of type {request.param}')
    client.start()

    # TODO: create rumor instance attached to this client!
    yield client

    print(f'closing client of type {request.param}')
    client.stop()


async def test_status(single_client):
    print(f'Client: {single_client}')
    assert True

    # lighthouse = LighthouseClient()
    # await lighthouse.start()
    # print('started lighthouse client')

    # rumor = Rumor()
    # await rumor.start(cmd='./bin/rumor')
    # print('started rumor')

    # l_actor = rumor.actor('lighthouse')
    # await l_actor.host.start().ok
    # await l_actor.host.listen(tcp=9000).ok
    # print('started l_actor')

    # peer_id = await l_actor.peer.connect(lighthouse.enr()).peer_id()
    # print(f'connected to lighthouse peer: {peer_id}')

    # l_status = Status(
    # version=GENESIS_FORK_VERSION,
    # finalized_root=GENESIS_ROOT,
    # finalized_epoch=0,
    # head_root=GENESIS_ROOT,
    # head_epoch=0,
    # )
    # l_status_resp = await l_actor.rpc.status.req.raw(peer_id, l_status.encode_bytes().hex(), raw=True).ok
    # assert l_status_resp['chunk']['result_code'] == 0
    # status = Status.decode_bytes(bytes.fromhex(l_status_resp['chunk']['data']))

    # TODO: test values
    # print(f'received status response: {status}')

    # await rumor.stop()
    # await lighthouse.stop()
    # print('stoped rumor')
