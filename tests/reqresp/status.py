from eth2spec.utils.ssz.ssz_typing import Container
from eth2spec.phase0.spec import Slot, Root, Epoch, ForkDigest
from sclients import connect_rumor

from ..utils import parse_chunk_response, with_rumor, enr_to_fork_digest


class Status(Container):
    fork_digest: ForkDigest
    finalized_root: Root
    finalized_epoch: Epoch
    head_root: Root
    head_slot: Slot


@with_rumor
async def run(rumor, args):
    peer_id = await connect_rumor(rumor, args['client'], args['enr'])

    logs = []
    return_code = 0

    fork_digest = enr_to_fork_digest(args['enr'])
    req_data = Status(fork_digest=fork_digest).encode_bytes().hex()
    req_call = rumor.rpc.status.req.raw(peer_id, req_data, raw=True, compression='snappy')
    await req_call
    await req_call.next()
    resp = await req_call.next()

    (resp_data, l) = parse_chunk_response(resp)
    logs.extend(l)
    if resp_data is None:
        return_code = 1

    else:
        resp_status = Status.decode_bytes(bytes.fromhex(resp_data))

        # TODO: make these dependent on beacon_state
        expected_status = Status(
            fork_digest=fork_digest,
            finalized_root='0x0000000000000000000000000000000000000000000000000000000000000000',
            finalized_epoch=0,
            head_root='0x2227ce1b4e15c6320d493998fab783190a50e71d1075af73ce4e9ccc0dc84bca',
            head_slot=0
        )

        if resp_status != expected_status:
            logs.append(f'response error: expected {expected_status}, got {resp_status}')
            return_code = 1

    return (return_code, logs)
