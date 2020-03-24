from remerkleable.complex import Container
from remerkleable.byte_arrays import Bytes32, Bytes4
from remerkleable.basic import uint64


class Version(Bytes4):
    pass


class Status(Container):
    version: Bytes4
    finalized_root: Bytes32
    finalized_epoch: uint64
    head_root: Bytes32
    head_slot: uint64
