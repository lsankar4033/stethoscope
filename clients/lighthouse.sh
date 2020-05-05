#!/bin/bash

docker pull sigp/lighthouse:latest

# TODO: expose port during creation
# TODO: specify port, address, privkey from args
# TODO: use args for single_client_genesis
docker create --name lighthouse sigp/lighthouse:latest bin/bash -c \
  "lcli --spec minimal new-testnet --testnet-dir /testnet --deposit-contract-address 0000000000000000000000000000000000000000 && \
  cp /genesis.ssz /testnet/genesis.ssz && \
  lighthouse bn --testnet-dir /testnet --spec minimal --dummy-eth1 --http --enr-match"

docker cp ssz/single_client_genesis.ssz lighthouse:/genesis.ssz
docker start lighthouse
# TODO: docker start container with port, address, args
