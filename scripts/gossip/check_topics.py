from pyrum import Rumor

EXPECTED_TOPICS = ["/eth2/beacon_block/ssz", "/eth2/beacon_attestation/ssz", "/eth2/voluntary_exit/ssz",
                   "/eth2/proposer_slashing/ssz", "/eth2/attester_slashing/ssz"]


async def check_topics(enr):
    async with Rumor(cmd='rumor') as rumor:
        print('Testing topics')
        await rumor.host.start()
        await rumor.gossip.start()

        peer_id = await rumor.peer.connect(enr).peer_id()

        for topic in EXPECTED_TOPICS:
            await rumor.gossip.join(topic)

            resp = await rumor.gossip.list_peers(topic)
            peers = resp['peers']

            assert peers == [peer_id]

        print('done')
