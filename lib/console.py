from colored import fg
from typing import NamedTuple


class ConsoleWriter(NamedTuple):
    suite: str
    fixture: str
    test: str

    def _prefix(self):
        if self.suite is None and self.fixture is None and self.test is None:
            return ''

        elif self.fixture is None and self.test is None:
            return f'{self.suite}'

        elif self.fixture is None:
            return f'{self.suite} -- {self.test}'

        elif self.test is None:
            return f'{self.suite}[{self.fixture}]'

        else:
            return f'{self.suite}[{self.fixture}] -- {self.test}'

    def info(self, s):
        print(f'{self._prefix()} {s}')

    def success(self, s):
        print(f"{self._prefix()} {fg('green')}{s}{fg('white')}")

    def fail(self, s):
        print(f"{self._prefix()} {fg('red')}{s}{fg('white')}")
