# stethoscope
Stethoscope is an Eth 2.0 scenario runner that works with real, running clients. 

Right now it's used for single-client regression tests. In the future, we hope to also use it to run multi-client scenarios as a tool for bug discovery.

## Background

If we're to have a mutli-client Eth 2.0 mainnet, we're going to need to do multi-client testing. Even though individual clients adhere to the [spec](https://github.com/ethereum/eth2.0-specs) and are rigorously tested internally, there are likely to be divergent assumptions in client implementation that only show up when multiple clients talk to each other.

Testnets will capture much of this, but they aren't the best tool for closely examining specific multi-client scenarios (called 'suites' in this project). Stethoscope aims to fill that gap. 

Suites are defined by:

1. the client instances involved
2. the rumor-driven scripts to run

and are defined in yaml, as seen [here](suites/single_client_genesis.yml).

Suites can refer to specific scripts to run, such as [this](https://github.com/lsankar4033/stethoscope/blob/master/scripts/reqresp/metadata.py).

## Single-client tests
This section will outline how to run the single-client tests in stethoscope.

### Usage

#### Prereqs
Install:

- [python3](https://wiki.python.org/moin/BeginnersGuide/Download)
- [pip](https://pip.pypa.io/en/stable/installing/)
- [rumor](https://github.com/protolambda/rumor)
- [docker](https://docs.docker.com/get-docker/)

#### Run locally
Clone the repo and install requirements:

```bash
$ git clone https://github.com/lsankar4033/stethoscope.git && cd stethoscope
...
$ pip install -r requirements.txt
```
Then, run a single test suite (in this case [single\_client\_genesis](tests/single_client_genesis.yml):

```bash
$ ./steth.py -s single_client_genesis
```

Or run all tests:

```bash
$ ./steth.py
```

### Tests
| description   |                         status                        |
|----------|:-----------------------------------------------------:|
| responds to all req/resp methods  | done        |
| subscribed to the right gossipsub topics     | done |
| running disc5 and is 'lookup-able' | in progress |
| client re-gossips messages | TODO | 

## Multi-client scenarios
TODO!

## Contributions
Contributions extremely welcome! Especially in the realm of test scenarios to examine

