from ..interfaces import IPower


class MockPower(IPower):
    def __init__(self, name=None):
        self.state = False
        self.name = name or self.__class__.__name__

    async def on(self):
        print('{}: ON'.format(self.name))
        self.state = True

    async def off(self):
        print('{}: OFF'.format(self.name))
        self.state = False

    async def is_on(self):
        return self.state
