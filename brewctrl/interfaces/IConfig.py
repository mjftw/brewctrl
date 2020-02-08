import abc
import asyncio


class MissingConfig(Exception):
    ''' Raised when trying to read from a config field that is not found '''
    pass


class IConfig(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    async def write(self, name: str, value):
        pass

    @abc.abstractmethod
    async def read(self, name: str):
        pass