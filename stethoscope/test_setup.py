from pyrum import Rumor

import asyncio
import pytest


@pytest.mark.asyncio
async def test_rumor_setup(event_loop):
    rumor = Rumor()
    await rumor.start(cmd='./bin/rumor')
    print('Started rumor')

    await rumor.stop()
    print('Stopped rumor')

    assert True
