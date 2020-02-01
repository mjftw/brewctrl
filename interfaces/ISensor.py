import abc
import asyncio


class ISensor(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def read(self):
        pass