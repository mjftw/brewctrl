import abc


class IPower(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    async def on(self):
        pass

    @abc.abstractmethod
    async def off(self):
        pass

    @abc.abstractmethod
    async def is_on(self):
        pass