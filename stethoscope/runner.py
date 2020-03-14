import asyncio
import json

from typing import List, Dict, AsyncGenerator, Any, Callable, Coroutine
from asyncio import Future, Queue as AsyncQueue
from io import BytesIO, TextIOWrapper

CallID = str


class Rumor(object):
    calls: Dict[CallID, "Call"]
    _unique_call_id_counter: int

    actors: Dict[str, "Actor"]

    def __init__(self):
        self.calls = {}
        self.actors = {}
        self._unique_call_id_counter = 0

    async def start(self):
        print("starting")
        self.rumor_process = await asyncio.create_subprocess_shell(
            'rumor',
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE)
        loop = asyncio.get_event_loop()

        async def read_loop(ru: Rumor):
            while True:
                line = await ru.rumor_process.stdout.readline()
                line = line.decode('utf-8')
                if line.endswith('\n'):
                    line = line[:-1]

                print('Received line from Rumor:' + str(line))

                try:
                    entry: Dict[str, Any] = json.loads(line)
                except Exception as e:
                    print(f"json decoding exception on input '{line}': {e}")
                    continue

                # find the corresponding call, pass on the event.
                if 'call_id' in entry:
                    call_id = entry['call_id']
                    if isinstance(call_id, str) and call_id.startswith('@'):
                        call_id = call_id[1:]
                        if call_id not in ru.calls:
                            continue

                        call: Call = ru.calls[call_id]
                        await call.on_entry(entry)
                        if call.ok.done() or call.ok.cancelled():
                            # call is over, remove it
                            del self.calls[call_id]

                # find the corresponding actor, pass on the event.
                if 'actor' in entry:
                    actor_name = entry['actor']
                    if actor_name not in ru.actors:
                        ru.actors[actor_name] = Actor(ru, actor_name)

                    actor = ru.actors[actor_name]
                    await actor.on_entry(entry)

        async def debug_loop(ru: Rumor):
            while True:
                line = await ru.rumor_process.stderr.readline()
                if line.endswith('\n'):
                    line = line[:-1]
                print(f"ERROR from Rumor: '{line}'")

        loop.create_task(debug_loop(self))
        loop.create_task(read_loop(self))

        print("done starting")

    def actor(self, name: str) -> "Cmd":
        return Actor(self, name)

    async def _send_to_rumor_process(self, line):
        inp = self.rumor_process.stdin
        print(f"Sending command to Rumor: '{line}'")
        inp.write((line + '\n').encode())
        await inp.drain()

    def make_call(self, args: List[str]) -> "Call":
        # Get a unique call ID
        call_id = f"py_${self._unique_call_id_counter}"
        self._unique_call_id_counter += 1
        # Create the call, and remember it
        cmd = ' '.join(args)
        call = Call(call_id, cmd)
        self.calls[call_id] = call
        # Send the actual command, with call ID, to Rumor
        asyncio.create_task(self._send_to_rumor_process(call_id + '> ' + cmd))
        return call

    # No actor, Rumor will just default to a default-actor.
    # But this is useful for commands that don't necessarily have any actor, e.g. debugging the contents of an ENR.
    def __getattr__(self, item) -> "Cmd":
        return Cmd(self, [item])


def args_to_call_path(*args, **kwargs) -> List[str]:
    # TODO: maybe escape values?
    return list(args) + [f'--{key}="{value}"' for key, value in kwargs.items()]


class Actor(object):

    def __init__(self, rumor: Rumor, name: str):
        self.rumor = rumor
        self.name = name
        self.q = AsyncQueue()

    def __call__(self, *args, **kwargs) -> "Call":
        return self.rumor.make_call([f'{self.name}:'] + args_to_call_path(*args, **kwargs))

    def __getattr__(self, item) -> "Cmd":
        return Cmd(self.rumor, [f'{self.name}:'] + [item])

    async def on_entry(self, entry: Dict[str, Any]):
        await self.q.put(entry)

    async def logs(self) -> AsyncGenerator:
        """Async generator to wait for and yield each log entry, including errors"""
        while True:
            v = await self.q.get()
            yield v


class Cmd(object):
    def __init__(self, rumor: Rumor, path: List[str]):
        self.rumor = rumor
        self.path = path

    def __call__(self, *args, **kwargs) -> "Call":
        return self.rumor.make_call(self.path + args_to_call_path(*args, **kwargs))

    def __getattr__(self, item) -> "Cmd":
        return Cmd(self.rumor, self.path + [item])


class CallException(Exception):
    def __init__(self, call_id: CallID, err_entry: Dict[str, Any]):
        self.call_id = call_id
        self.err_entry = err_entry


class Call(object):
    data: Dict[str, Any]
    cmd: str
    # Future to wait for command to complete, future raises exception if any error entry makes it first.
    ok: Future

    def __init__(self, call_id: CallID, cmd: str):
        self.data = {}
        self.call_id = call_id
        self.cmd = cmd
        self.ok = Future()
        self.q = AsyncQueue()

    async def on_entry(self, entry: Dict[str, Any]):
        # Log the entry, if call is being monitored
        await self.q.put(entry)

        # Merge in new result data, overwrite any previous data
        for k, v in entry.items():
            self.data[k] = v

        # Complete call future with exception
        if entry['level'] == 'error':
            self.ok.set_exception(CallException(self.call_id, entry))
            return
        # Complete call future as normal
        if '@success' in entry:  # special key, present in last log, after command completes
            self.ok.set_result(None)
            return

    async def logs(self) -> AsyncGenerator:
        """Async generator to wait for and yield each log entry, including errors"""
        while True:
            v = await self.q.get()
            yield v

    def __getattr__(self, item) -> Callable[[], Coroutine]:
        async def attr_fut():
            await self.ok
            return self.data[item]

        return attr_fut


# Not sure yet how tests will be packaged.
# Also need each test to live isolated from other tests
# (simulated network, fresh client instance to test against, etc.).
async def basic_connect_example():
    rumor = Rumor()
    await rumor.start()

    alice = rumor.actor('alice')
    await alice.host.start().ok
    # Flags are keyword arguments
    await alice.host.listen(tcp=9000).ok

    bob = rumor.actor('bob')
    await bob.host.start().ok
    await bob.host.listen(tcp=9001).ok

    # Getting a result should be as easy as calling, and waiting for the key we are after
    bob_addr = await bob.host.view().enr()

    # Or alternatively, collect all result data from the call:
    # bob_host_data = await bob.host.view().ok
    # bob_addr = bob_host_data['enr']

    # Print all ENR contents
    await rumor.enr.view(bob_addr).ok

    # Command arguments are just call arguments
    await alice.peer.connect(bob_addr).ok


asyncio.run(basic_connect_example())
