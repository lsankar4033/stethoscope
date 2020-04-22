FROM sigp/lighthouse:latest

ARG PORT=9000
ENV PORT ${PORT}

ARG ADDRESS=0.0.0.0
ENV ADDRESS ${ADDRESS}

ARG PRIVKEY=0xEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE
ENV PRIVKEY ${PRIVKEY}

ARG GENESIS_PATH=ssz/genesis.ssz

COPY $GENESIS_PATH /genesis.ssz

EXPOSE $PORT

RUN ["/usr/local/bin/lcli", "--spec", "minimal", "new-testnet"]

# TODO: why doesn't this work?
#CMD /user/local/bin/lighthouse  \
      #bn \
      #--testnet-dir /root/.lighthouse/testnet \
      #--listen-ADDRESS ${ADDRESS} \
      #--PORT ${PORT} \
      #--p2p-PRIVKEY ${PRIVKEY} \
      #testnet \
      #--spec minimal \
      #-r quick 8 1584657416

CMD ["/usr/local/bin/lighthouse", \
      "bn", \
      "--testnet-dir", "/root/.lightouse/testnet", \
      "--listen-address", "${ADDRESS}", \
      "--port", "${PORT}", \
      "--p2p-priv-key", "${PRIVKEY}", \
      "testnet", \
      "--spec", "minimal", \
      "-f", "file", "ssz", "/genesis.ssz"]
