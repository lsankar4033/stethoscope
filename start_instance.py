def start_instance(client, enr, genesis):
    if client != 'test':
        raise ValueError('only test clients supported at the moment')

    return subprocess.Popen(
        ['lighthouse', 'bn', '--listen-address', self.address, '--port',
         str(self.port), '--p2p-priv-key', self.privkey, 'testnet', '--spec', 'minimal', '-f', 'file', 'ssz', self.genesis_path],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
