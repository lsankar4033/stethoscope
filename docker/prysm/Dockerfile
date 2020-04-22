FROM gcr.io/prysmaticlabs/prysm/beacon-chain:latest

ARG GENESIS_PATH=ssz/genesis.ssz

COPY $GENESIS_PATH /genesis.ssz

# TODO: necessary port input

# config that seems to work locally:
#bazel run //beacon-chain --define ssz=minimal -- \
#--datadir /tmp/chaindata \
#--force-clear-db \
#--interop-genesis-state /tmp/genesis.ssz \
#--interop-eth1data-votes \
#--min-sync-peers=0

CMD ["--rpc-port", "4001", \
      "--p2p-udp-port", "12001", \
      "--p2p-tcp-port", "13001", \
      "--custom-genesis-delay", "12", \
      "--interop-genesis-state", "/genesis.ssz", \
      "--interop-eth1data-votes", \
      "--min-sync-peers", "0", \
      "--bootstrap-node", "", \
      "--web3provider", \
      "--http-web3provider"]
      #"--datadir", "/", \

