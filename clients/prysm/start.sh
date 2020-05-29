#-!/bin/bash
#
# Startup script for the prysm client

# TODO: use an image name that's passed in! To allow multiple lighthouse clients
# Default values of arguments
TCP=9000
UDP=9001
IP='127.0.0.1'
PRIVATE_KEY='eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee'
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

# Create prysm container
docker pull gcr.io/prysmaticlabs/prysm/beacon-chain:latest
docker create --name prysm -p $TCP:$TCP -p $UDP:$UDP gcr.io/prysmaticlabs/prysm/beacon-chain \
  --minimal-config \
  --interop-genesis-state /beacon_state.ssz \
  --p2p-host-ip $IP
  #--p2p-priv-key /privkey.txt \
  #--p2p-tcp-port $TCP \
  #--p2p-udp-port $UDP

# Copy beacon state file into the container
docker cp $BEACON_STATE_PATH prysm:/beacon_state.ssz

# Copy private key into key file in container
#echo $PRIVATE_KEY > ./tmp.txt
#docker cp ./tmp.txt prysm:/privkey.txt
#rm ./tmp.txt

# Start the container
docker start prysm

#bin/bash -c \
  #"lcli --spec minimal new-testnet --testnet-dir /testnet --deposit-contract-address 0000000000000000000000000000000000000000 && \
  #cp /genesis.ssz /testnet/genesis.ssz && \
  #lighthouse bn --testnet-dir /testnet \
    #--spec minimal \
    #--dummy-eth1 \
    #--port $TCP \
    #--enr-udp-port $UDP \
    #--enr-address $IP \
    #--p2p-priv-key $PRIVATE_KEY"


