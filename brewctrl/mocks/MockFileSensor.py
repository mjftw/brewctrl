from ast import literal_eval

from ..interfaces import ISensor


class MockFileSensor(ISensor):
    def __init__(self, filename):
        self.filename = filename

    async def read(self):
        with open(self.filename, 'r') as f:
            return literal_eval(f.read())