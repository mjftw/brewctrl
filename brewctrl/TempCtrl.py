import asyncio
from datetime import datetime
from .interfaces import ITempCtrl, IStorage, ISensor, IPower, IEventStream
from enum import Enum


class ControllerState(Enum):
    IDLE = 0
    HEATING = 1
    COOLING = 2
    ERROR = 3


class TempCtrl(ITempCtrl):
    def __init__(self,
            refresh_period_s: int,
            storage: IStorage,
            temp_sensor: ISensor,
            hot_power: IPower,
            cold_power: IPower,
            event_stream: IEventStream=None
        ):
        assert isinstance(storage, IStorage)
        assert isinstance(temp_sensor, ISensor)
        assert isinstance(hot_power, IPower)
        assert isinstance(cold_power, IPower)
        assert isinstance(event_stream, IEventStream) or event_stream is None

        self.storage = storage
        self.temp_sensor = temp_sensor
        self.hot_power = hot_power
        self.cold_power = cold_power
        self.refresh_period_s = refresh_period_s
        self.event_stream = event_stream

        self._running = False
        self._state = ControllerState.IDLE

    async def _send_event(self, event_name, data):
        if self.event_stream:
            asyncio.ensure_future(self.event_stream.put(event_name, data))

    async def get_setpoint(self):
        return await self.storage.read_int('setpoint')

    async def set_setpoint(self, setpoint):
        await self._send_event('set_setpoint', setpoint)
        await self.storage.write_int('setpoint', setpoint)

    async def get_temperature(self):
        data = await self.temp_sensor.read()
        await self._send_event('temperature', data)
        return data

    async def get_tolerance(self):
        return await self.storage.read_int('tolerance')

    async def set_tolerance(self, tolerance):
        await self._send_event('set_tolerance', tolerance)
        return await self.storage.write_int('tolerance', tolerance)

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
        temperature = await self.get_temperature()
        setpoint = await self.get_setpoint()
        tolerance = await self.get_tolerance()
        state = await self.get_state()
        next_state = state

        if self._state == ControllerState.COOLING:
            if temperature <= setpoint:
                next_state = ControllerState.IDLE

        elif self._state == ControllerState.IDLE:
            if temperature >= setpoint + tolerance:
                next_state = ControllerState.COOLING
            elif temperature <= setpoint - tolerance:
                next_state = ControllerState.HEATING

        elif self._state == ControllerState.HEATING:
            if temperature >= setpoint:
                next_state = ControllerState.IDLE

        if next_state != state:
            asyncio.ensure_future(self.set_state(next_state))

    async def get_state(self):
        cold_on = await self.cold_power.is_on()
        hot_on = await self.hot_power.is_on()

        if cold_on:
            if hot_on:
                return ControllerState.ERROR
            else:
                return ControllerState.COOLING
        else:
            if hot_on:
                return ControllerState.HEATING
            else:
                return ControllerState.IDLE


    async def set_state(self, state: ControllerState):
        if state == ControllerState.COOLING:
            await self.cold_power.on()
            await self.hot_power.off()
            await self._send_event('change_state', 'cooling')
        elif state == ControllerState.IDLE:
            await self.cold_power.off()
            await self.hot_power.off()
            await self._send_event('change_state', 'idle')
        elif state == ControllerState.HEATING:
            await self.cold_power.off()
            await self.hot_power.on()
            await self._send_event('change_state', 'heating')


