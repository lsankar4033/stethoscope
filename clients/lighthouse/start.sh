#!/bin/bash

docker pull sigp/lighthouse:latest

# TODO: use a name that's passed in! To allow multiple lighthouse clients
# TODO: use args for single_client_genesis, port(s), address, privkey
docker create --name lighthouse -p 9000:9000 -p 9001:9001 sigp/lighthouse:latest bin/bash -c \
  "lcli --spec minimal new-testnet --testnet-dir /testnet --deposit-contract-address 0000000000000000000000000000000000000000 && \
  cp /genesis.ssz /testnet/genesis.ssz && \
  lighthouse bn --testnet-dir /testnet --spec minimal --dummy-eth1 \
    --enr-tcp-port 9000 \
    --enr-udp-port 9001 \
    --enr-address 127.0.0.1 \
    --p2p-priv-key 0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee"

docker cp ssz/single_client_genesis.ssz lighthouse:/genesis.ssz
docker start lighthouse
