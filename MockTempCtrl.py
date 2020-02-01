import asyncio
from random import randint

from ITempCtrl import ITempCtrl


class MockTempCtrl(ITempCtrl):
    def __init__(self):
        self._setpoint = 18

    @property
    def setpoint(self):
        return self._setpoint

    @setpoint.setter
    def setpoint(self, setpoint):
        self._setpoint = setpoint

    @property
    async def get_temperature(self):
        return self.setpoint + randint(00, 20)/10 - 1
