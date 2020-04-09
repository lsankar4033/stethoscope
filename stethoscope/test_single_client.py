from pyrum import Rumor

import os
import pytest

from stethoscope.clients.clients import build_client
from stethoscope.genesis_state import load_genesis_state, spec, write_genesis_state
from stethoscope.reqresp import Status

GENESIS_PATH = 'ssz/genesis.ssz'

ENV = os.environ.get('STETHOSCOPE_ENV') or 'development'


@pytest.fixture(scope='session')
def genesis_path():
    print(f'writing new genesis file at {GENESIS_PATH}')

    # Don't rewrite cached file unless in production
    if ENV == 'production' or not os.path.isfile(GENESIS_PATH):
        write_genesis_state(GENESIS_PATH)

    yield GENESIS_PATH

    if ENV == 'production':
        os.remove(GENESIS_PATH)


def clients():
    return ['lighthouse'] if ENV == 'development' else ['docker_lighthouse']


@pytest.fixture(scope='session', params=clients())
def client(request, genesis_path):
    client = build_client(request.param, genesis_path)

    print(f'starting client of type {request.param}\n')
    client.start()

    yield client

    print(f'closing client of type {request.param}\n')
    client.stop()


# NOTE: trio fixture
@pytest.fixture
async def single_client_rumor(client):
    print('starting rumor instance')
    # TODO: install rumor on travis-ci
    async with Rumor(cmd='rumor') as rumor:
        await rumor.host.start()
        await rumor.host.listen(tcp=9001)
        print('set up rumor instance')

        print(f'attempting to connect to client with ENR {client.enr()}')
        client_id = await rumor.peer.connect(client.enr()).peer_id()
        print(f'connected rumor to client with peer ID {client_id}')

        yield (rumor, client_id)


# Tests that client started up properly
def test_client_startup(client):
    import time
    time.sleep(0.5)  # TODO: Do something better here
    assert client.is_running()


async def test_status_rpc(single_client_rumor, genesis_path):
    state = load_genesis_state(genesis_path)
    req_status = Status(
        version=spec.GENESIS_FORK_VERSION,
        finalized_root='0x0000000000000000000000000000000000000000000000000000000000000000',
        finalized_epoch=0,
        head_root='0x0000000000000000000000000000000000000000000000000000000000000000',
        head_epoch=0
    )
    req = req_status.encode_bytes().hex()

    rumor, client_id = single_client_rumor
    resp = await rumor.rpc.status.req.raw(client_id, req, raw=True)
    resp_status = Status.decode_bytes(bytes.fromhex(resp['chunk']['data']))

    assert resp_status == Status(
        version=spec.GENESIS_FORK_VERSION,
        finalized_root='0x0000000000000000000000000000000000000000000000000000000000000000',
        finalized_epoch=0,
        head_root='0xef64a1b94652cd9070baa4f9c0e8b1ce624bdb071b77b51b1a54b8babb1a5cd2',
        head_epoch=0
    )
