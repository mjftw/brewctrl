from ..interfaces import IStorage


class MockStorage(IStorage):
    def __init__(self):
        self.data = {}

    async def read_int(self, name):
        try:
            value = self.data[name]
        except KeyError:
            value = 0
        print(f'{self.__class__.__name__}: Read {name}={value}')
        return value

    async def write_int(self, name, value):
        print(f'{self.__class__.__name__}: Write {name}={value}')
        self.data[name] = value
