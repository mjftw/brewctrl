import asyncio
from .interfaces import ITempCtrl, IStorage, ISensor


class TempCtrl(ITempCtrl):
    def __init__(self, storage: IStorage, temp_sensor: ISensor):
        assert isinstance(storage, IStorage)
        assert isinstance(temp_sensor, ISensor)
        self.storage = storage
        self.temp_sensor = temp_sensor

    async def get_setpoint(self):
        return await self.storage.read_int('setpoint')

    async def set_setpoint(self, setpoint):
        await self.storage.write_int('setpoint', setpoint)

    async def get_temperature(self):
        return await self.temp_sensor.read()
