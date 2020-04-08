import subprocess


class SubprocessException(Exception):
    def __init__(self, completed_process):
        self.completed_process = completed_process


class DockerException(Exception):
    def __init__(self, msg):
        self.msg = msg


# TODO: extract out common abstract base class for clients (w/shared methods, etc.)

class DockerLighthouseClient:
    def __init__(self, genesis_path):
        self.genesis_path = genesis_path
        self.address = '0.0.0.0'
        self.port = 9000
        self.privkey = '0xEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE'

        self.process = None
        self.container_id = None

    # NOTE: assumes port 9000!
    # TODO: compute from our own parameters
    def enr(self):
        return 'enr:-Iu4QIS99y_PyET83eyeAsS463grgYSm1tY6KaVljNjMMZhfFbqo2X0lXe8Lu19O_njq3-EZV9_dhiun5dJ4jOp5uVIBgmlkgnY0gmlwhH8AAAGJc2VjcDI1NmsxoQOnBq2PcxFfkFACZvJz91cd-UKaTPtLv7zYJSJyAtq60YN0Y3CCIyiDdWRwgiMo'

    def _create_container(self):
        # TODO: make sure this is what we expect
        out = subprocess.run(
            ['docker', 'create', '-p', '9000:9000', 'sigp/lighthouse', 'lighthouse', 'bn', '--listen-address', self.address, '--port',
                str(self.port), '--p2p-priv-key', self.privkey, 'testnet', '--spec', 'minimal', '-f', 'file', 'ssz', 'genesis.ssz'],
            capture_output=True
        )
        if out.returncode != 0:
            raise SubprocessException(out)

        self.container_id = str(out.stdout.strip(), 'utf-8')

    def _copy_genesis_to_container(self):
        if self.container_id is None:
            raise DockerException("Can't move genesis file to container before container is created")

        out = subprocess.run(
            ['docker', 'cp', self.genesis_path, f'{self.container_id}:/genesis.ssz'],
            capture_output=True
        )
        if out.returncode != 0:
            raise SubprocessException(out)

    def _run_container(self):
        if self.container_id is None:
            raise DockerException("Can't run container before it's created")

        self.process = subprocess.Popen(
            ['docker', 'start', f'{self.container_id}'],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

    def logs(self):
        if self.container_id is None:
            raise DockerException("Can't retrieve logs for non-existent container")

        out = subprocess.run(
            ['docker', 'logs', self.container_id],
            capture_output=True
        )
        return out.stdout

    def start(self):
        self._create_container()
        self._copy_genesis_to_container()
        self._run_container()

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
