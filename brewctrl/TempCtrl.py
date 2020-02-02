import asyncio
from datetime import datetime
from .interfaces import ITempCtrl, IStorage, ISensor, IPower


class TempCtrl(ITempCtrl):
    def __init__(self,
            refresh_period_s: int,
            storage: IStorage,
            temp_sensor: ISensor,
            hot_power: IPower=None,
            cold_power: IPower=None,
        ):
        assert isinstance(storage, IStorage)
        assert isinstance(temp_sensor, ISensor)
        assert isinstance(hot_power, IPower) or hot_power is None
        assert isinstance(cold_power, IPower) or cold_power is None

        self.storage = storage
        self.temp_sensor = temp_sensor
        self.hot_power = hot_power
        self.cold_power = cold_power
        self.refresh_period_s = refresh_period_s

        self._running = False

    async def get_setpoint(self):
        return await self.storage.read_int('setpoint')

    async def set_setpoint(self, setpoint):
        await self.storage.write_int('setpoint', setpoint)

    async def get_temperature(self):
        return await self.temp_sensor.read()

    async def start(self):
        self._running = True

        while self._running:
            start_time = datetime.now()
            await self.update()

            sleep_time = max(0,
                self.refresh_period_s - (datetime.now() - start_time).seconds)
            await asyncio.sleep(sleep_time)

    async def stop(self):
        self._running = False

    async def update(self):
        print('Update')
        if not self.hot_power and not self.cold_power:
            # No control, so nothing to do
            return

        temp = await self.temp_sensor.read()
        setpoint = await self.get_setpoint()

        if temp > setpoint:
            if self.hot_power:
                await self.hot_power.off()
            if self.cold_power:
                await self.cold_power.on()
        elif temp < setpoint:
            if self.hot_power:
                await self.hot_power.on()
            if self.cold_power:
                await self.cold_power.off()


