import os
import asyncio

from .interfaces import ISensor

class SensorError(Exception):
    pass


class W1TempSensor(ISensor):
    w1_bus_path = '/sys/bus/w1/devices'
    # Known Sensors:
    #   28-02029245757f
    #   28-021792455c61
    def __init__(self, serialno):
        self.serialno = serialno
        self.read_path = os.path.join(W1TempSensor.w1_bus_path, self.serialno, 'w1_slave')

    async def read(self):
        for __ in range(0, 10):
            data = await self._get_raw_data()

            if 'YES' in data:
                return await self._extract_temp(data)

            asyncio.sleep(0.1)

        raise SensorError('Failed to read sensor: {}'.format(self.serialno))

    async def _extract_temp(self, data):
        idx = data[1].find('t=') + 2
        if idx == -1:
            raise SensorError('Invalid data read from sensor:\n {data}')
        else:
            return (float)(data[1][idx:].strip())/1000

    async def _get_raw_data(self):
        if not os.path.isfile(self.read_path):
            raise SensorError('Cannot find file at {}'.format(self.read_path))

        with open(self.read_path, 'r') as f:
            return f.readlines()
