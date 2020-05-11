# stethoscope
Stethoscope is a suite of networking tests for eth2 beacon-chain clients that are designed to be readable and runnable by anyone.

## Overview
Consistency in basic client networking is an important challenge to solve to get to a multi-client Eth2 mainnet. There are already some [great](https://github.com/protolambda/rumor) [tools](https://github.com/prrkl/docs/blob/master/project-overview.md) that are client agnostic and allow manual network debugging/testing.

Stethoscope is complementary to these tools in the same way that the eth2spec is complementary to client implementations. It's both:

1. a repository of test cases
2. a test runner to run said test cases

Tests are grouped by the 'fixture' of client instances required to set them up (to allow re-use of a set of instances). As an example, see the [single\_client\_genesis](tests/single_client_genesis.yml) group. 

Each test is identified by a python script (i.e. [the gossip topic membership test](https://github.com/lsankar4033/stethoscope/blob/master/scripts/gossip/topic_membership.py)) that uses [rumor](https://github.com/protolambda/rumor) to drive clients behind the scenes. 

## Usage

### Prereqs
Install:

- [python3](https://wiki.python.org/moin/BeginnersGuide/Download)
- [pip](https://pip.pypa.io/en/stable/installing/)
- [rumor](https://github.com/protolambda/rumor)
- [docker](https://docs.docker.com/get-docker/)

### Run locally
Clone the repo and install requirements:

```bash
$ https://github.com/lsankar4033/stethoscope.git && cd stethoscope
...
$ pip install -r requirements.txt

```
Then, run a single test suite (in this case [single\_client\_genesis](tests/single_client_genesis.yml):

```bash
$ python run.py single_client_genesis
```

Or run all tests:

```bash
$ python run.py
```

## Testing plan and progress
There are two classes of tests that stethoscope is intended to cover:

1. sanity checks
2. edge cases discovered by other testing

The former are things like how a single client responds to valid or invalid messages on each network domain and the latter are more nuanced edge cases that come out of other testing efforts and conversations.

### 1

| type   | test             |                         status                        |
|----------|-----------------------|:-----------------------------------------------------:|
| req/resp | valid responses for each request  | [done](tests/single_client_genesis.yml#L15-46)        |
| gossip   | expected topic membership      | [done](tests/single_client_genesis.yml#L33-37)        |
| feature   | snappy compression enabled      | TODO        |
| feature   | noise encryption enabled      | TODO        |

Still need to add tests for discv5, more gossip tests. please share ideas!

### 2

TODO! If you have ideas, please make a github issue! Note that multi-client tests are possible.

## Client start/stop scripts

Each client needs bash scripts for starting and stopping, as seen for lighthouse [here](https://github.com/lsankar4033/stethoscope/tree/master/clients/lighthouse).

These scripts need to take [initialization parameters](https://github.com/lsankar4033/stethoscope/blob/master/tests/single_client_genesis.yml#L3-L11) as input. This allows started instances to be discoverable by their tests and to have a predictable beacon state.

## Contributions
Contributions extremely welcome! Especially in the realm of:

1. new test cases
2. scripts to run each client


## Acknowledgements

