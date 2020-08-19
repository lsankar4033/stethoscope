from enum import auto, Enum


class BeaconState(Enum):
    DEFAULT = auto()


# NOTE: when network_config is specifiable, it needs to be an arg here
def default_builder():
    from eth2spec.config.config_util import prepare_config
    prepare_config('config', 'minimal')

    from eth2spec.phase0.spec import initialize_beacon_state_from_eth1
    from eth2spec.test.helpers.deposits import prepare_genesis_deposits

    import eth2fastspec as spec

    deposits, deposit_root, _ = prepare_genesis_deposits(
        spec, spec.MIN_GENESIS_ACTIVE_VALIDATOR_COUNT, spec.MAX_EFFECTIVE_BALANCE, signed=True)

    eth1_block_hash = b'\x12' * 32
    eth1_timestamp = spec.MIN_GENESIS_TIME
    state = initialize_beacon_state_from_eth1(eth1_block_hash, eth1_timestamp, deposits)

    return state


BEACON_STATE_BUILDERS = {
    BeaconState.DEFAULT: default_builder
}

BEACON_STATE_PATHS = {
    BeaconState.DEFAULT: 'ssz/default.ssz'
}
