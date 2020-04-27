from abc import abstractmethod, ABC
from yaml import load, Loader

import subprocess


class Client(ABC):
    def __init__(self, client_type):
        with open(f'config/clients/{client_type}.yml', 'r') as r:
            self.config = load(r, Loader=Loader)

    # TODO: actually implement this. Right now just defaults to the ENR found in simple_minimal config
    def enr(self):
        return 'enr:-Iu4QIS99y_PyET83eyeAsS463grgYSm1tY6KaVljNjMMZhfFbqo2X0lXe8Lu19O_njq3-EZV9_dhiun5dJ4jOp5uVIBgmlkgnY0gmlwhH8AAAGJc2VjcDI1NmsxoQOnBq2PcxFfkFACZvJz91cd-UKaTPtLv7zYJSJyAtq60YN0Y3CCIyiDdWRwgiMo'

    @abstractmethod
    def start(self):
        ...

    @abstractmethod
    def stop(self):
        ...

    # NOTE: just for startup test
    @abstractmethod
    def is_running(self):
        ...


# NOTE: this is the placeholder. client teams should replace it with something specific
class DefaultClient(Client):
    def __init__(self, client_type):
        self.process = None
        super().__init__(client_type)

    def start(self):
        self.process = subprocess.Popen(
            ['lighthouse', 'bn',
                '--listen-address', self.config['ip'],
                '--port', str(self.config['tcp_port']),
                '--p2p-priv-key', self.config['privkey'],
                'testnet',
                '--spec', 'minimal',
                '-f', 'file', 'ssz', self.config['genesis']],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

    def stop(self):
        if self.process is None or not self.is_running():
            return

        self.process.terminate()

    # NOTE: just for startup test
    def is_running(self):
        return self.process is not None and self.process.poll() is None


def build_client(client_type):
    return DefaultClient(client_type)
