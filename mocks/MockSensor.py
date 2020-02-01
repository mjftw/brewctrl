from random import randint

from ..interfaces import ISensor


class MockSensor(ISensor):
    async def read(self):
        return randint(0, 101)