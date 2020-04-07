from pyrum import Rumor

import os
import pytest
import trio

from stethoscope.clients import build_client
from stethoscope.genesis_state import write_genesis_state


GENESIS_PATH = 'ssz/genesis.ssz'

ENV = os.environ.get('STETHOSCOPE_ENV') or 'development'


@pytest.fixture(scope='session')
def genesis_path(request):
    print(f'writing new genesis file at {GENESIS_PATH}')

    # Don't rewrite cached file unless in production
    if ENV == 'production' or not os.path.isfile(GENESIS_PATH):
        write_genesis_state(GENESIS_PATH)

    yield GENESIS_PATH

    if ENV == 'production':
        os.remove(GENESIS_PATH)


# NOTE: this isn't the right abstraction when we consider multiple genesis files and more complicated (i.e.
# multi-client tests)
@pytest.fixture(scope='session', params=['lighthouse'])
def single_client(request, genesis_path):
    client = build_client(request.param, genesis_path)

    print(f'starting client of type {request.param}\n')
    client.start()

    # TODO: create rumor instance attached to this client!
    yield client

    print(f'closing client of type {request.param}\n')
    client.stop()


async def test_status(single_client):
    # async with rumor (decorator)
    # connect rumor <-> client (helper fn?)
    # try status message on rumor
    # check response
    print(f'Client: {single_client}')
    assert True
