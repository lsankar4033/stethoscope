import trio
from pyrum import SubprocessConn, Rumor

from .utils import with_rumor

@with_rumor
async def run(rumor, args):
    return 0
