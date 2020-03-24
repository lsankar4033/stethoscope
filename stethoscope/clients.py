import asyncio


class LighthouseClient:

    # TODO: make these specifiable
    def __init__(self):
        self.address = '0.0.0.0'
        self.port = 9000
        self.privkey = '0xEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE'
        self.process = None

    def enr(self):
        return '-Iu4QIS99y_PyET83eyeAsS463grgYSm1tY6KaVljNjMMZhfFbqo2X0lXe8Lu19O_njq3-EZV9_dhiun5dJ4jOp5uVIBgmlkgnY0gmlwhH8AAAGJc2VjcDI1NmsxoQOnBq2PcxFfkFACZvJz91cd-UKaTPtLv7zYJSJyAtq60YN0Y3CCIyiDdWRwgiMo'

    # NOTE: replace with docker cmd when I put in Travis
    def _run_cmd(self):
        return f'lighthouse bn --listen-address {self.address} --port {self.port} --p2p-priv-key {self.privkey} testnet -r quick 8 $(date +%s)'

    async def start(self):
        self.process = await asyncio.create_subprocess_shell(self._run_cmd())

    async def stop(self):
        if self.process is None:
            return

        self.process.terminate()
        await self.process.wait()
