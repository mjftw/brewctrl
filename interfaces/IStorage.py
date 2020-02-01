import abc
import asyncio


class IStorage(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    async def write_int(self, name: str, value: int):
        pass

    @abc.abstractmethod
    async def read_int(self, name: str) -> int:
        pass