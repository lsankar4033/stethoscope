from eth2spec.utils.ssz.ssz_typing import (
    View, boolean, Container, List, Vector, uint64,
    Bytes1, Bytes4, Bytes8, Bytes32, Bytes48, Bytes96, Bitlist, Bitvector,
)


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
MAX_COMMITTEES_PER_SLOT = 2**6
TARGET_COMMITTEE_SIZE = 2**7
MAX_VALIDATORS_PER_COMMITTEE = 2**11
MIN_PER_EPOCH_CHURN_LIMIT = 2**2
CHURN_LIMIT_QUOTIENT = 2**16
SHUFFLE_ROUND_COUNT = 90
MIN_GENESIS_ACTIVE_VALIDATOR_COUNT = 2**14
MIN_GENESIS_TIME = 1578009600
MIN_DEPOSIT_AMOUNT = Gwei(2**0 * 10**9)
MAX_EFFECTIVE_BALANCE = Gwei(2**5 * 10**9)
EJECTION_BALANCE = Gwei(2**4 * 10**9)
EFFECTIVE_BALANCE_INCREMENT = Gwei(2**0 * 10**9)
GENESIS_FORK_VERSION = Version('0x00000000')
BLS_WITHDRAWAL_PREFIX = Bytes1('0x00')
MIN_GENESIS_DELAY = 86400
SECONDS_PER_SLOT = 12
MIN_ATTESTATION_INCLUSION_DELAY = 2**0
SLOTS_PER_EPOCH = 2**5
MIN_SEED_LOOKAHEAD = 2**0
MAX_SEED_LOOKAHEAD = 2**2
MIN_EPOCHS_TO_INACTIVITY_PENALTY = 2**2
SLOTS_PER_ETH1_VOTING_PERIOD = 2**10
SLOTS_PER_HISTORICAL_ROOT = 2**13
MIN_VALIDATOR_WITHDRAWABILITY_DELAY = 2**8
PERSISTENT_COMMITTEE_PERIOD = 2**11
EPOCHS_PER_HISTORICAL_VECTOR = 2**16
EPOCHS_PER_SLASHINGS_VECTOR = 2**13
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
ETH1_FOLLOW_DISTANCE = 2**10
TARGET_AGGREGATORS_PER_COMMITTEE = 2**4
RANDOM_SUBNETS_PER_VALIDATOR = 2**0
EPOCHS_PER_RANDOM_SUBNET_SUBSCRIPTION = 2**8
SECONDS_PER_ETH1_BLOCK = 14


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
