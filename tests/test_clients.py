import os
import subprocess

from pyrum import SubprocessConn, Rumor
import trio

from lib.fixtures import start_instance, stop_instance
from lib.types import ENR, InstanceConfig


BEACON_STATE_LOCATION = 'ssz/tests.ssz'

# NOTE: currently identical to the ENR in single_client_genesis suite, but maybe not this in the future
TEST_ENR_DICT = {
    'enr': 'enr:-LK4QJCIZoViytOOmAzAbdOJODwQ36PhjXwvXlTFTloTzpawVpvPRmtrM6UZdPmOGck5yPZ9AbgmwyZnE3jm4jX0Yx0Bh2F0dG5ldHOIAAAAAAAAAACEZXRoMpBGMkSJAAAAAf__________gmlkgnY0gmlwhH8AAAGJc2VjcDI1NmsxoQOnBq2PcxFfkFACZvJz91cd-UKaTPtLv7zYJSJyAtq60YN0Y3CCIyiDdWRwgiMp',
    'private_key': '0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee',
    'udp': 9001,
    'tcp': 9000,
    'id': 'v4',
    'ip': '127.0.0.1',
    'attnets': '0x0000000000000000',
    'eth2': '0x4632448900000001ffffffffffffffff'
}
TEST_ENR = ENR(**TEST_ENR_DICT)


def write_beacon_state():
    from eth2spec.config.config_util import prepare_config
    prepare_config('tests/config', 'minimal')

    from eth2spec.phase0.spec import initialize_beacon_state_from_eth1
    from eth2spec.test.helpers.deposits import prepare_genesis_deposits

    import eth2fastspec as spec

    print('preparing genesis deposits')
    deposits, deposit_root, _ = prepare_genesis_deposits(
        spec, spec.MIN_GENESIS_ACTIVE_VALIDATOR_COUNT, spec.MAX_EFFECTIVE_BALANCE, signed=True)

    print('initializing beacon state')
    eth1_block_hash = b'\x12' * 32
    eth1_timestamp = spec.MIN_GENESIS_TIME
    state = initialize_beacon_state_from_eth1(eth1_block_hash, eth1_timestamp, deposits)

    print('writing beacon state')
    os.makedirs(os.path.dirname(BEACON_STATE_LOCATION), exist_ok=True)
    with open(BEACON_STATE_LOCATION, 'wb') as w:
        state.serialize(w)

    return state


async def connect_rumor(rumor, enr):
    # NOTE: duplicated in scripts/lib.py
    await rumor.host.start()
    peer_id = await rumor.peer.connect(enr).peer_id()
    return peer_id


async def test_lighthouse():
    config = InstanceConfig('lighthouse', BEACON_STATE_LOCATION, TEST_ENR)
    start_instance(config)

    try:
        async with SubprocessConn(cmd='rumor bare') as conn:
            async with trio.open_nursery() as nursery:
                rumor = Rumor(conn, nursery)
                peer_id = await connect_rumor(rumor, TEST_ENR.enr)
                print(f'lighthouse peer_id: {peer_id}')

                # NOTE: this may not be the exact test
                assert peer_id is not None
                nursery.cancel_scope.cancel()

    finally:
        stop_instance(config)


async def test_prysm():
    config = InstanceConfig('prysm', BEACON_STATE_LOCATION, TEST_ENR)

    start_instance(config)

    try:
        async with SubprocessConn(cmd='rumor bare') as conn:
            async with trio.open_nursery() as nursery:
                rumor = Rumor(conn, nursery)
                peer_id = await connect_rumor(rumor, TEST_ENR.enr)
                print(f'prysm peer_id: {peer_id}')

                # NOTE: this may not be the exact test
                assert peer_id is not None
                nursery.cancel_scope.cancel()

    finally:
        stop_instance(config)
