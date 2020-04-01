from eth2spec.utils.ssz.ssz_typing import (
    View, boolean, Container, List, Vector, uint64,
    Bytes1, Bytes4, Bytes8, Bytes32, Bytes48, Bytes96, Bitlist, Bitvector,
)


# NOTE: all of the following code taken from pyspec + test helpers


def build_deposit_data(spec, pubkey, privkey, amount, withdrawal_credentials, signed=False):
    deposit_data = spec.DepositData(
        pubkey=pubkey,
        withdrawal_credentials=withdrawal_credentials,
        amount=amount,
    )
    if signed:
        sign_deposit_data(spec, deposit_data, privkey)
    return deposit_data


def build_deposit(spec,
                  deposit_data_list,
                  pubkey,
                  privkey,
                  amount,
                  withdrawal_credentials,
                  signed):
    deposit_data = build_deposit_data(spec, pubkey, privkey, amount, withdrawal_credentials, signed=signed)
    index = len(deposit_data_list)
    deposit_data_list.append(deposit_data)
    return deposit_from_context(spec, deposit_data_list, index)


def deposit_from_context(spec, deposit_data_list, index):
    deposit_data = deposit_data_list[index]
    root = hash_tree_root(List[spec.DepositData, 2**spec.DEPOSIT_CONTRACT_TREE_DEPTH](*deposit_data_list))
    tree = calc_merkle_tree_from_leaves(tuple([d.hash_tree_root() for d in deposit_data_list]))
    proof = list(get_merkle_proof(tree, item_index=index, tree_len=32)) + [(index + 1).to_bytes(32, 'little')]
    leaf = deposit_data.hash_tree_root()
    assert spec.is_valid_merkle_branch(leaf, proof, spec.DEPOSIT_CONTRACT_TREE_DEPTH + 1, index, root)
    deposit = spec.Deposit(proof=proof, data=deposit_data)

    return deposit, root, deposit_data_list


def prepare_genesis_deposits(spec, genesis_validator_count, amount, signed=False, deposit_data_list=None):
    if deposit_data_list is None:
        deposit_data_list = []
    genesis_deposits = []
    for validator_index in range(genesis_validator_count):
        pubkey = pubkeys[validator_index]
        privkey = privkeys[validator_index]
        # insecurely use pubkey as withdrawal key if no credentials provided
        withdrawal_credentials = spec.BLS_WITHDRAWAL_PREFIX + spec.hash(pubkey)[1:]
        deposit, root, deposit_data_list = build_deposit(
            spec,
            deposit_data_list,
            pubkey,
            privkey,
            amount,
            withdrawal_credentials,
            signed,
        )
        genesis_deposits.append(deposit)

    return genesis_deposits, root, deposit_data_list


def build_genesis_state():
    # NOTE: taken from pyspec
    eth1_block_hash = b'\x12' * 32
    eth1_timestamp = MIN_GENESIS_TIME

    deposits, deposit_root, _ = prepare_genesis_deposits(
        spec, MIN_GENESIS_ACTIVE_VALIDATOR_COUNT, MAX_EFFECTIVE_BALANCE, signed=True)

    fork = Fork(
        previous_version=GENESIS_FORK_VERSION,
        current_version=GENESIS_FORK_VERSION,
        epoch=GENESIS_EPOCH,
    )

    beacon_block = BeaconBlockBody()

    state = BeaconState(
        genesis_time=eth1_timestamp - eth1_timestamp % MIN_GENESIS_DELAY + 2 * MIN_GENESIS_DELAY,
        fork=fork,
        eth1_data=Eth1Data(block_hash=eth1_block_hash, deposit_count=0),
        latest_block_header=BeaconBlockHeader(body_root=beacon_block.hash_tree_root()),
        randao_mixes=[eth1_block_hash] * EPOCHS_PER_HISTORICAL_VECTOR,  # Seed RANDAO with Eth1 entropy
    )

    # TODO: process deposits

    return state


# NOTE: actual type code follows


class Slot(uint64):
    pass


class Epoch(uint64):
    pass


class CommitteeIndex(uint64):
    pass


class ValidatorIndex(uint64):
    pass


class Gwei(uint64):
    pass


class Root(Bytes32):
    pass


class Version(Bytes4):
    pass


class DomainType(Bytes4):
    pass


class Domain(Bytes8):
    pass


class BLSPubkey(Bytes48):
    pass


class BLSSignature(Bytes96):
    pass


# NOTE: this is mainnet spec. Should be minimal
########
# Config
########
GENESIS_SLOT = Slot(0)
GENESIS_EPOCH = Epoch(0)
FAR_FUTURE_EPOCH = Epoch(2**64 - 1)
BASE_REWARDS_PER_EPOCH = 4
DEPOSIT_CONTRACT_TREE_DEPTH = 2**5
JUSTIFICATION_BITS_LENGTH = 4
ENDIANNESS = 'little'
MAX_VALIDATORS_PER_COMMITTEE = 2**11
MIN_PER_EPOCH_CHURN_LIMIT = 2**2
CHURN_LIMIT_QUOTIENT = 2**16
MIN_GENESIS_TIME = 1578009600
MIN_DEPOSIT_AMOUNT = Gwei(2**0 * 10**9)
MAX_EFFECTIVE_BALANCE = Gwei(2**5 * 10**9)
EJECTION_BALANCE = Gwei(2**4 * 10**9)
EFFECTIVE_BALANCE_INCREMENT = Gwei(2**0 * 10**9)
BLS_WITHDRAWAL_PREFIX = Bytes1('0x00')
MIN_ATTESTATION_INCLUSION_DELAY = 2**0
MIN_SEED_LOOKAHEAD = 2**0
MAX_SEED_LOOKAHEAD = 2**2
MIN_EPOCHS_TO_INACTIVITY_PENALTY = 2**2
SLOTS_PER_ETH1_VOTING_PERIOD = 2**10
MIN_VALIDATOR_WITHDRAWABILITY_DELAY = 2**8
HISTORICAL_ROOTS_LIMIT = 2**24
VALIDATOR_REGISTRY_LIMIT = 2**40
BASE_REWARD_FACTOR = 2**6
WHISTLEBLOWER_REWARD_QUOTIENT = 2**9
PROPOSER_REWARD_QUOTIENT = 2**3
INACTIVITY_PENALTY_QUOTIENT = 2**25
MIN_SLASHING_PENALTY_QUOTIENT = 2**5
MAX_PROPOSER_SLASHINGS = 2**4
MAX_ATTESTER_SLASHINGS = 2**0
MAX_ATTESTATIONS = 2**7
MAX_DEPOSITS = 2**4
MAX_VOLUNTARY_EXITS = 2**4
DOMAIN_BEACON_PROPOSER = DomainType('0x00000000')
DOMAIN_BEACON_ATTESTER = DomainType('0x01000000')
DOMAIN_RANDAO = DomainType('0x02000000')
DOMAIN_DEPOSIT = DomainType('0x03000000')
DOMAIN_VOLUNTARY_EXIT = DomainType('0x04000000')
SAFE_SLOTS_TO_UPDATE_JUSTIFIED = 2**3
TARGET_AGGREGATORS_PER_COMMITTEE = 2**4
RANDOM_SUBNETS_PER_VALIDATOR = 2**0
EPOCHS_PER_RANDOM_SUBNET_SUBSCRIPTION = 2**8
SECONDS_PER_ETH1_BLOCK = 14

GENESIS_EPOCH = Epoch(0)

# made minimal
GENESIS_FORK_VERSION = Version('0x00000001')
MIN_GENESIS_DELAY = 300
MAX_COMMITTEES_PER_SLOT = 4
TARGET_COMMITTEE_SIZE = 4
SHUFFLE_ROUND_COUNT = 10
MIN_GENESIS_ACTIVE_VALIDATOR_COUNT = 64
ETH1_FOLLOW_DISTANCE = 16
SECONDS_PER_SLOT = 6
SLOTS_PER_EPOCH = 8
EPOCHS_PER_ETH1_VOTING_PERIOD = 2
SLOTS_PER_HISTORICAL_ROOT = 64
PERSISTENT_COMMITTEE_PERIOD = 128
MAX_EPOCHS_PER_CROSSLINK = 4
EPOCHS_PER_HISTORICAL_VECTOR = 64
EPOCHS_PER_SLASHINGS_VECTOR = 64
PHASE_1_FORK_VERSION = 0x01000001
INITIAL_ACTIVE_SHARDS = 4
MAX_SHARDS = 8
EARLY_DERIVED_SECRET_PENALTY_MAX_FUTURE_EPOCHS = 4096


class Fork(Container):
    previous_version: Version
    current_version: Version
    epoch: Epoch  # Epoch of latest fork


class Checkpoint(Container):
    epoch: Epoch
    root: Root


class Validator(Container):
    pubkey: BLSPubkey
    withdrawal_credentials: Bytes32  # Commitment to pubkey for withdrawals
    effective_balance: Gwei  # Balance at stake
    slashed: boolean
    # Status epochs
    activation_eligibility_epoch: Epoch  # When criteria for activation were met
    activation_epoch: Epoch
    exit_epoch: Epoch
    withdrawable_epoch: Epoch  # When validator can withdraw funds


class AttestationData(Container):
    slot: Slot
    index: CommitteeIndex
    # LMD GHOST vote
    beacon_block_root: Root
    # FFG vote
    source: Checkpoint
    target: Checkpoint


class IndexedAttestation(Container):
    attesting_indices: List[ValidatorIndex, MAX_VALIDATORS_PER_COMMITTEE]
    data: AttestationData
    signature: BLSSignature


class PendingAttestation(Container):
    aggregation_bits: Bitlist[MAX_VALIDATORS_PER_COMMITTEE]
    data: AttestationData
    inclusion_delay: Slot
    proposer_index: ValidatorIndex


class Eth1Data(Container):
    deposit_root: Root
    deposit_count: uint64
    block_hash: Bytes32


class HistoricalBatch(Container):
    block_roots: Vector[Root, SLOTS_PER_HISTORICAL_ROOT]
    state_roots: Vector[Root, SLOTS_PER_HISTORICAL_ROOT]


class DepositMessage(Container):
    pubkey: BLSPubkey
    withdrawal_credentials: Bytes32
    amount: Gwei


class DepositData(Container):
    pubkey: BLSPubkey
    withdrawal_credentials: Bytes32
    amount: Gwei
    signature: BLSSignature  # Signing over DepositMessage


class BeaconBlockHeader(Container):
    slot: Slot
    parent_root: Root
    state_root: Root
    body_root: Root


class SigningRoot(Container):
    object_root: Root
    domain: Domain


class AttesterSlashing(Container):
    attestation_1: IndexedAttestation
    attestation_2: IndexedAttestation


class Attestation(Container):
    aggregation_bits: Bitlist[MAX_VALIDATORS_PER_COMMITTEE]
    data: AttestationData
    signature: BLSSignature


class Deposit(Container):
    proof: Vector[Bytes32, DEPOSIT_CONTRACT_TREE_DEPTH + 1]  # Merkle path to deposit root
    data: DepositData


class VoluntaryExit(Container):
    epoch: Epoch  # Earliest epoch when voluntary exit can be processed
    validator_index: ValidatorIndex


class SignedBeaconBlockHeader(Container):
    message: BeaconBlockHeader
    signature: BLSSignature


class ProposerSlashing(Container):
    proposer_index: ValidatorIndex
    signed_header_1: SignedBeaconBlockHeader
    signed_header_2: SignedBeaconBlockHeader


class VoluntaryExit(Container):
    epoch: Epoch  # Earliest epoch when voluntary exit can be processed
    validator_index: ValidatorIndex


class SignedVoluntaryExit(Container):
    message: VoluntaryExit
    signature: BLSSignature


class BeaconState(Container):
    # Versioning
    genesis_time: uint64
    slot: Slot
    fork: Fork
    # History
    latest_block_header: BeaconBlockHeader
    block_roots: Vector[Root, SLOTS_PER_HISTORICAL_ROOT]
    state_roots: Vector[Root, SLOTS_PER_HISTORICAL_ROOT]
    historical_roots: List[Root, HISTORICAL_ROOTS_LIMIT]
    # Eth1
    eth1_data: Eth1Data
    eth1_data_votes: List[Eth1Data, SLOTS_PER_ETH1_VOTING_PERIOD]
    eth1_deposit_index: uint64
    # Registry
    validators: List[Validator, VALIDATOR_REGISTRY_LIMIT]
    balances: List[Gwei, VALIDATOR_REGISTRY_LIMIT]
    # Randomness
    randao_mixes: Vector[Bytes32, EPOCHS_PER_HISTORICAL_VECTOR]
    # Slashings
    slashings: Vector[Gwei, EPOCHS_PER_SLASHINGS_VECTOR]  # Per-epoch sums of slashed effective balances
    # Attestations
    previous_epoch_attestations: List[PendingAttestation, MAX_ATTESTATIONS * SLOTS_PER_EPOCH]
    current_epoch_attestations: List[PendingAttestation, MAX_ATTESTATIONS * SLOTS_PER_EPOCH]
    # Finality
    justification_bits: Bitvector[JUSTIFICATION_BITS_LENGTH]  # Bit set for every recent justified epoch
    previous_justified_checkpoint: Checkpoint  # Previous epoch snapshot
    current_justified_checkpoint: Checkpoint
    finalized_checkpoint: Checkpoint


class BeaconBlockBody(Container):
    randao_reveal: BLSSignature
    eth1_data: Eth1Data  # Eth1 data vote
    graffiti: Bytes32  # Arbitrary data
    # Operations
    proposer_slashings: List[ProposerSlashing, MAX_PROPOSER_SLASHINGS]
    attester_slashings: List[AttesterSlashing, MAX_ATTESTER_SLASHINGS]
    attestations: List[Attestation, MAX_ATTESTATIONS]
    deposits: List[Deposit, MAX_DEPOSITS]
    voluntary_exits: List[SignedVoluntaryExit, MAX_VOLUNTARY_EXITS]
