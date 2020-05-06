# stethoscope
Stethoscope is a suite of networking tests for eth2 beacon-chain clients that are designed to be readable and runnable by anyone.

## Overview
Network testing is a 'last mile' problem  that needs to be solved before Eth2 gets to Phase 0 mainnet. There are already some [great](https://github.com/protolambda/rumor) [tools](https://github.com/prrkl/docs/blob/master/project-overview.md) that are client agnostic and allow manual network debugging/testing.

Stethoscope is complementary to these tools in the same way that the eth2spec is complementary to implementation efforts. It serves as a living repository of test cases along with a way for anyone to run them and verify that things are working as expected.

Tests are grouped by the instance group required to set them up. For an example, see the [single\_client\_genesis](tests/single_client_genesis.yml) group. See [here](#test-config-format) for more on the format of these files.

## Usage

### Prereqs
- python3
- pip


### Run locally
Clone the repo and install requirements:

```bash
$ https://github.com/lsankar4033/stethoscope.git && cd stethoscope
...
$ pip install -r requirements.txt

```
Then, run a single test suite (in this case [single\_client\_genesis](tests/single_client_genesis.yml):

```bash
$ python run_test.py tests/single_client_genesis.yml
```

<!--Or run all tests:-->

<!--```bash-->
<!--$ python run_tests.py-->
<!--```-->

Note that by default the test will run with my 'test' eth2 client, which is an old lighthouse binary. As scripts to run the various clients are added to [clients/](clients/), the test suites will be runnable against all of them.

## Testing plan and progress
There are two classes of tests that stethoscope is intended to cover:

1. sanity checks
2. edge cases discovered by other testing

The former are things like how a single client responds to valid or invalid messages on each network domain and the latter are more nuanced edge cases that come out of other testing efforts and conversations.

### 1

_TODO_: add remaining TODO tests (invalid messages, more gossip, discv5 tests)

| domain   | test name             |                         status                        |
|----------|-----------------------|:-----------------------------------------------------:|
| req/resp | valid status request  | [done](tests/single_client_genesis.yml#L12-17)        |
| req/resp | valid blocks-by-range | [done](tests/single_client_genesis.yml#L19-24)        |
| req/resp | valid blocks-by-root  | [in progress](tests/single_client_genesis.yml#L26-31) |
| req/resp | valid ping            | TODO                                                  |
| gossip   | topic membership      | [done](tests/single_client_genesis.yml#L33-37)        |

### 2

TODO

## Contributions
Contributions extremely welcome! Especially in the realm of:

1. new test cases
2. scripts to run each client

For 1, please file an issue describing any suggestions and for 2, please submit PRs to this repo.


## Test config format
TODO
