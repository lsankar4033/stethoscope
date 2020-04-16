from stethoscope.clients.lighthouse import LighthouseClient, DockerLighthouseClient


# TODO: use unused ports for subsequent clients to be safe
def build_client(client_type, genesis_path):
    if client_type == 'lighthouse':
        return LighthouseClient(genesis_path, 9000)

    elif client_type == 'docker_lighthouse':
        return DockerLighthouseClient(genesis_path, 9000)

    else:
        raise ValueError(f"Unknown client type: {client_type}")
