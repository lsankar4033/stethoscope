import subprocess

from stethoscope.clients.client import Client


class PrysmClient(Client):
    def __init__(self, genesis_path, port):
        Client.__init__(self, genesis_path, port)

    def start(self):
        ...
