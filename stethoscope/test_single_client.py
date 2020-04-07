from pyrum import Rumor

import os
import pytest

from stethoscope.clients import build_client
from stethoscope.genesis_state import write_genesis_state

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


# NOTE: below, 'client' and 'rumor' may be renamed once we include multi-client tests as well as these
# single-client ones

@pytest.fixture(scope='session', params=['lighthouse'])
def client(request, genesis_path):
    client = build_client(request.param, genesis_path)

    print(f'starting client of type {request.param}\n')
    client.start()

    yield client

    print(f'closing client of type {request.param}\n')
    client.stop()


# NOTE: trio fixture
@pytest.fixture
async def rumor(client):
    print('starting rumor instance')
    async with Rumor(cmd='rumor') as rumor:
        await rumor.host.start()
        await rumor.host.listen(tcp=9001)
        print('set up rumor instance')

        print(f'attempting to connect to client with ENR {client.enr()}')
        client_id = await rumor.peer.connect(client.enr()).peer_id()
        print(f'connected rumor to client with peer ID {client_id}')

        yield rumor


# async def test_client_startup(client):
    #assert client.is_running()

# async def test_status_rpc(rumor):
    # async with rumor (decorator)
    # connect rumor <-> client (helper fn?)
    # try status message on rumor
    # check response
    #print(f'Rumor: {rumor}')
    #assert True
