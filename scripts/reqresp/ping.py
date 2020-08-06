import trio
from eth2spec.utils.ssz.ssz_typing import uint64
from pyrum import SubprocessConn, Rumor
from sclients import connect_rumor

from ..utils import parse_response, with_rumor


@with_rumor
async def run(rumor, args):
    peer_id = await connect_rumor(rumor, args['enr'])

    return_code = 0
    for i in range(5):
        req = uint64(i).encode_bytes().hex()
        resp = await rumor.rpc.ping.req.raw(peer_id, req, raw=True, compression='snappy')
        (rc, resp_data) = parse_response(resp)
        if rc != 0:
            return_code = rc
            continue

        pong = uint64.decode_bytes(bytes.fromhex(resp_data))

        if not isinstance(pong, int) or pong < 0:
            return_code = 1

    return return_code
