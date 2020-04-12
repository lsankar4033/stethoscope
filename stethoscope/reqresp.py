from eth2spec.utils.ssz.ssz_typing import (
    Bytes4, Bytes32, Container, uint64
)

from eth2spec.phase0.spec import Root, Slot


class Status(Container):
    version: Bytes4
    finalized_root: Bytes32
    finalized_epoch: uint64
    head_root: Bytes32
    head_slot: uint64


class BlocksByRangeReqV1(Container):
    head_block_root: Root
    start_slot: Slot
    count: uint64
    step: uint64


class BlocksByRangeReqV2(Container):
    start_slot: Slot
    count: uint64
    step: uint64
