import subprocess

from stethoscope.clients.client import Client


class SubprocessException(Exception):
    def __init__(self, completed_process):
        self.completed_process = completed_process


class DockerException(Exception):
    def __init__(self, msg):
        self.msg = msg


class DockerLighthouseClient(Client):
    def __init__(self, genesis_path, port):
        Client.__init__(self, genesis_path, port)

    def _build_image(self):
        subprocess.run(
            ['docker', 'build',
                '-f', 'docker/lighthouse/Dockerfile',
                '-t', 'stethoscope/lighthouse',
                '--build-arg', f'GENESIS_PATH={self.genesis_path}',
                '--build-arg', f'ADDRESS={self.address}',
                '--build-arg', f'PORT={self.port}',
                '--build-arg', f'PRIVKEY={self.privkey}',
                '.']
        )

    def _run_image(self):
        self.process = subprocess.Popen(
            ['docker', 'run', 'stethoscope/lighthouse:latest'],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

    def start(self):
        self._build_image()
        self._run_image()


class LighthouseClient(Client):
    def __init__(self, genesis_path, port):
        Client.__init__(self, genesis_path, port)

    def start(self):
        self.process = subprocess.Popen(
            ['lighthouse', 'bn', '--listen-address', self.address, '--port',
                str(self.port), '--p2p-priv-key', self.privkey, 'testnet', '--spec', 'minimal', '-f', 'file', 'ssz', self.genesis_path],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
