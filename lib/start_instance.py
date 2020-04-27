import eth_utils

from lib.enr import ENR


def format_ip(ip):
    return ".".join([str(n) for n in ip])


def start_instance(client, enr_str, genesis):
    if client != 'test':
        raise ValueError('only test clients supported at the moment')

    enr = ENR.from_repr(enr_str)

    ip_address = format_ip(enr.get(b'ip'))
    port = str(enr.get(b'tcp'))
    privkey = eth_utils.to_hex(enr.get(b'secp256k1'))

    # NOTE: this is what happens to work locally for me
    return subprocess.Popen(
        ['lighthouse', 'bn',
            '--listen-address', ip_address,
            '--port', port,
            '--p2p-priv-key', privkey,
            'testnet', '--spec', 'minimal', '-f', 'file', 'ssz', genesis],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
