import abc

class IEventStream(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    async def put(self, event_name, data):
        pass
