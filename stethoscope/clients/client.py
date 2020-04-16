class Client:
    def __init__(self, genesis_path, port):
        self.genesis_path = genesis_path
        self.address = '0.0.0.0'
        self.port = port
        self.privkey = '0xEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE'

        self.process = None

    # TODO: actually implement this
    def enr(self):
        return 'enr:-Iu4QIS99y_PyET83eyeAsS463grgYSm1tY6KaVljNjMMZhfFbqo2X0lXe8Lu19O_njq3-EZV9_dhiun5dJ4jOp5uVIBgmlkgnY0gmlwhH8AAAGJc2VjcDI1NmsxoQOnBq2PcxFfkFACZvJz91cd-UKaTPtLv7zYJSJyAtq60YN0Y3CCIyiDdWRwgiMo'

    def start(self):
        ...

    def stop(self):
        if self.process is None or not self.is_running():
            return

        self.process.terminate()

    def is_running(self):
        return self.process is not None and self.process.poll() is None
