BLANK_GENESIS_ROOT = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'

from eth2spec.utils.ssz.ssz_typing import (
    Bytes4, Bytes32, Container, uint64
)


class Status(Container):
    # TODO: move to reqresp file or something
    version: Bytes4
    finalized_root: Bytes32
    finalized_epoch: uint64
    head_root: Bytes32
    head_slot: uint64
