from eth2spec.utils.ssz.ssz_typing import (
    Bytes4, Bytes32, Container, uint64
)


class Status(Container):
    version: Bytes4
    finalized_root: Bytes32
    finalized_epoch: uint64
    head_root: Bytes32
    head_slot: uint64
