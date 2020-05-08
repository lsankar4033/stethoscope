from pyrum import SubprocessConn, Rumor

import argparse
import trio


async def connect_rumor(rumor, enr):
    await rumor.host.start()
    peer_id = await rumor.peer.connect(enr).peer_id()
    return peer_id


def parse_args(*args):
    parser = argparse.ArgumentParser()
    req_grp = parser.add_argument_group(title='required')

    for arg in args:
        req_grp.add_argument(arg, required=True)

    return parser.parse_args()
