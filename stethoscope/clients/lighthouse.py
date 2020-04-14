import subprocess


class SubprocessException(Exception):
    def __init__(self, completed_process):
        self.completed_process = completed_process


class DockerException(Exception):
    def __init__(self, msg):
        self.msg = msg


class DockerLighthouseClient:
    def __init__(self, genesis_path):
        self.genesis_path = genesis_path
        self.address = '0.0.0.0'
        self.port = 9000
        self.privkey = '0xEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE'

        self.process = None

    # TODO: compute from our own parameters
    def enr(self):
        return 'enr:-Iu4QIS99y_PyET83eyeAsS463grgYSm1tY6KaVljNjMMZhfFbqo2X0lXe8Lu19O_njq3-EZV9_dhiun5dJ4jOp5uVIBgmlkgnY0gmlwhH8AAAGJc2VjcDI1NmsxoQOnBq2PcxFfkFACZvJz91cd-UKaTPtLv7zYJSJyAtq60YN0Y3CCIyiDdWRwgiMo'

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

    def stop(self):
        if self.process is None or not self.is_running():
            return

        self.process.terminate()

    def is_running(self):
        return self.process.poll() is None


class LighthouseClient:
    def __init__(self, genesis_path):
        # TODO: make these specifiable
        self.genesis_path = genesis_path
        self.address = '0.0.0.0'
        self.port = 9000
        self.privkey = '0xEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE'

        self.process = None

    # TODO: compute from our own parameters
    def enr(self):
        return 'enr:-Iu4QIS99y_PyET83eyeAsS463grgYSm1tY6KaVljNjMMZhfFbqo2X0lXe8Lu19O_njq3-EZV9_dhiun5dJ4jOp5uVIBgmlkgnY0gmlwhH8AAAGJc2VjcDI1NmsxoQOnBq2PcxFfkFACZvJz91cd-UKaTPtLv7zYJSJyAtq60YN0Y3CCIyiDdWRwgiMo'

    def start(self):
        self.process = subprocess.Popen(
            ['lighthouse', 'bn', '--listen-address', self.address, '--port',
                str(self.port), '--p2p-priv-key', self.privkey, 'testnet', '--spec', 'minimal', '-f', 'file', 'ssz', self.genesis_path],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

    def stop(self):
        if self.process is None or not self.is_running():
            return

        self.process.terminate()

    def is_running(self):
        return self.process.poll() is None
