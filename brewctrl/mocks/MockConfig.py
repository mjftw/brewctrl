from ..interfaces import IConfig


class MockConfig(IConfig):
    def __init__(self):
        self.data = {}

    async def read(self, name):
        try:
            value = self.data[name]
        except KeyError:
            value = 0
        print(f'{self.__class__.__name__}: Read {name}={value}')
        return value

    async def write(self, name, value):
        print(f'{self.__class__.__name__}: Write {name}={value}')
        self.data[name] = value
