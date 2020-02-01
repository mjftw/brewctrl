import abc
import asyncio

class ITempCtrl(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    async def set_setpoint(self, setpoint):
        pass

    @abc.abstractmethod
    async def get_setpoint(self):
        pass

    @abc.abstractmethod
    async def get_temperature(self):
        pass