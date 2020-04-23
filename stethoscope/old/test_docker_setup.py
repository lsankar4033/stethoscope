import subprocess


def test_docker():
    out = subprocess.run(['docker', 'ps'], capture_output=True)
    assert out.returncode == 0


def test_docker_pull():
    out = subprocess.run(['docker', 'run', 'sigp/lighthouse', 'lighthouse', '--help'], capture_output=True)
    assert out.returncode == 0
