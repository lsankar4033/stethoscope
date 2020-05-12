#!/bin/bash
#
# Startup script for the lighthouse client

# TODO: use an image name that's passed in! To allow multiple lighthouse clients
# Default values of arguments
TCP=9000
UDP=9001
IP='127.0.0.1'
PRIVATE_KEY='0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee'
BEACON_STATE_PATH='ssz/single_client_genesis.ssz'

# Parse arguments
for arg in "$@"
do
    case $arg in
      -t=*|--tcp=*)
        TCP="${arg#*=}"
        shift
        ;;
      -u|--udp=*)
        UDP="${arg#*=}"
        shift
        ;;
      -i|--ip=*)
        IP="${arg#*=}"
        shift
        ;;
      -p|--private-key=*)
        PRIVATE_KEY="${arg#*=}"
        shift
        ;;
      -b|--beacon-state-path=*)
        BEACON_STATE_PATH="${arg#*=}"
        shift
        ;;
    esac
done

# Create lighthouse container
docker pull sigp/lighthouse:latest
docker create --name lighthouse -p $TCP:$TCP -p $UDP:$UDP sigp/lighthouse:latest bin/bash -c \
  "lcli --spec minimal new-testnet --testnet-dir /testnet --deposit-contract-address 0000000000000000000000000000000000000000 && \
  cp /genesis.ssz /testnet/genesis.ssz && \
  lighthouse bn --testnet-dir /testnet \
    --spec minimal \
    --dummy-eth1 \
    --port $TCP \
    --enr-udp-port $UDP \
    --enr-address $IP \
    --p2p-priv-key $PRIVATE_KEY"

# Copy beacon state file into the container
docker cp $BEACON_STATE_PATH lighthouse:/genesis.ssz

# Start the container
docker start lighthouse
