from eth2spec.utils.ssz.ssz_typing import uint64
from sclients import connect_rumor

from ..utils import parse_chunk_response, with_rumor


@with_rumor
async def run(rumor, args):
    peer_id = await connect_rumor(rumor, args['client'], args['enr'])

    logs = []
    return_code = 0

    req_data = uint64(0).encode_bytes().hex()
    req_call = rumor.rpc.ping.req.raw(peer_id, req_data, raw=True, compression='snappy')
    await req_call
    await req_call.next()
    resp = await req_call.next()

    (resp_data, l) = parse_chunk_response(resp)
    logs.extend(l)
    if resp_data is None:
        return_code = 1

    else:
        pong = uint64.decode_bytes(bytes.fromhex(resp_data))

        if not isinstance(pong, int) or pong < 0:
            logs.append(f'invalid ping response: {pong}')
            return_code = 1

    return (return_code, logs)
