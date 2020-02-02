from ..interfaces import IPower


class MockPower(IPower):
    def __init__(self, name=None):
        self.state = False
        self.name = name or self.__class__.__name__

    async def on(self):
        print(f'{self.name}: ON')
        self.state = True

    async def off(self):
        print(f'{self.name}: OFF')
        self.state = False

    async def is_on(self):
        return self.state
