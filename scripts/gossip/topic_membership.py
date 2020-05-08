from pyrum import Rumor
from pyrum import SubprocessConn, Rumor
from ..utils import parse_args, connect_rumor

import trio

EXPECTED_TOPICS = ["/eth2/beacon_block/ssz", "/eth2/beacon_attestation/ssz", "/eth2/voluntary_exit/ssz",
                   "/eth2/proposer_slashing/ssz", "/eth2/attester_slashing/ssz"]


async def check_topics(enr):
    async with SubprocessConn(cmd='rumor bare') as conn:
        async with trio.open_nursery() as nursery:
            rumor = Rumor(conn, nursery)
            peer_id = await connect_rumor(rumor, enr)

            await rumor.gossip.start()

            peer_id = await rumor.peer.connect(enr).peer_id()

            for topic in EXPECTED_TOPICS:
                await rumor.gossip.join(topic)

                resp = await rumor.gossip.list_peers(topic)
                peers = resp['peers']

                assert peers == [peer_id]

            nursery.cancel_scope.cancel()

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    req_grp = parser.add_argument_group(title='required')
    req_grp.add_argument('--enr', required=True)

    args = parser.parse_args()

    trio.run(check_topics, args.enr)
