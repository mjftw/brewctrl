import asyncio
from random import randint

from ..interfaces import ITempCtrl, IConfig


class MockTempCtrl(ITempCtrl):
    def __init__(self):
        self._setpoint = 18

    async def set_setpoint(self, setpoint):
        self._setpoint = setpoint

    async def get_setpoint(self):
        return self._setpoint

    async def get_temperature(self):
        return self._setpoint + randint(00, 20)/10 - 1

    async def start(self, refresh_period_s):
        pass

    async def stop(self):
        pass
