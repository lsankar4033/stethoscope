# stethoscope
See [here](https://hackmd.io/t7aT3kQMS2S6me4Zo1CT3A?view) for the plan.

New structure:
- clients/ where client startup scripts live
- tests/ where tests are defined (yml files)
- scripts/ where scripts that tests run (and probably share) are defined
  - maybe also where genesis writing files live?
- ssz/ where genesis files live (referred by tests)

In this model, each file in tests/ corresponds to a *single test setup*. For example, it's assumed that the
clients in 'instances' will only be started once. 'all' can be used here for something that should be run
against every client.
