from collections import defaultdict
from typing import List, NamedTuple

from sclients import InstanceConfig, ENR

from lib.instance_configs import DEFAULT_ENR
from lib.beacon_state import BeaconState, BEACON_STATE_PATHS

# NOTE: this will hold network configs in the future
TEST_FILE_TO_CONFIGS = {
    'tests/reqresp/metadata.py': [BeaconState.DEFAULT],
    'tests/reqresp/ping.py': [BeaconState.DEFAULT],
    'tests/reqresp/status.py': [BeaconState.DEFAULT],
}


class TestGroup(NamedTuple):
    test_files: List[str]
    instance_config: InstanceConfig

    def __str__(self):
        return f'{self.instance_config.client} - {self.instance_config.beacon_state_path}'


# TODO: allow for comma-separated test filter
def file_matches_filter(file, file_filter):
    return file_filter is None or file == file_filter


# NOTE: this file does sorting
def get_test_groups(test_file_to_configs, clients, test_file_filter) -> List[TestGroup]:
    client_path_to_test_files = defaultdict(list)
    for test_file, beacon_states in test_file_to_configs.items():
        if file_matches_filter(test_file, test_file_filter):
            for client in clients:
                for beacon_state in beacon_states:
                    beacon_state_path = BEACON_STATE_PATHS[beacon_state]
                    client_path_to_test_files[(client, beacon_state_path)].append(test_file)

    test_groups = []
    for (client, beacon_state_path), test_files in client_path_to_test_files.items():
        instance_config = InstanceConfig(client, beacon_state_path, ENR(**DEFAULT_ENR))
        test_groups.append(TestGroup(test_files, instance_config))

    test_groups.sort(key=lambda tg: (tg.instance_config.client, tg.instance_config.beacon_state_path))

    return test_groups
