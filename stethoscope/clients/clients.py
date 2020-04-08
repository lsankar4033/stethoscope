from stethoscope.clients.lighthouse import LighthouseClient, DockerLighthouseClient


def build_client(client_type, genesis_path):
    if client_type == 'lighthouse':
        return LighthouseClient(genesis_path)

    elif client_type == 'docker_lighthouse':
        return DockerLighthouseClient(genesis_path)

    else:
        raise ValueError(f"Unknown client type: {client_type}")
