from random import randint

from ..interfaces import ISensor


class MockSensor(ISensor):
    async def read(self):
        value = randint(0, 101)
        print(f'{self.__class__.__name__}: {value}')
        return value