from ..interfaces import IPower


class MockPower(IPower):
    def __init__(self):
        self.state = False

    async def on(self):
        print(f'{self.__class__.__name__}: ON')
        self.state = True

    async def off(self):
        print(f'{self.__class__.__name__}: OFF')
        self.state = False

    async def is_on(self):
        return self.state
