from eth2spec.utils.ssz.ssz_typing import uint64, Bitvector, Container
from sclients import connect_rumor

from ..utils import parse_chunk_response, with_rumor

class Metadata(Container):
    seq_number: uint64
    attnets: Bitvector[64]


@with_rumor
async def run(rumor, args):
    peer_id = await connect_rumor(rumor, args['client'], args['enr'])

    logs = []
    return_code = 0

    req_call = rumor.rpc.metadata.req.raw(peer_id, '', raw=True, compression='snappy')
    await req_call
    await req_call.next()
    resp = await req_call.next()

    (resp_data, l) = parse_chunk_response(resp)
    logs.extend(l)
    if resp_data is None:
        return_code = 1

    else:
        # TODO: sanity checks on metadata
        metadata = Metadata.decode_bytes(bytes.fromhex(resp_data))

    return (return_code, logs)
