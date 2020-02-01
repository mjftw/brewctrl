from ..interfaces import IStorage


class MockStorage(IStorage):
    def __init__(self):
        self.data = {}

    async def read_int(self, name):
        return self.data[name]

    async def write_int(self, name, value):
        self.data[name] = value
