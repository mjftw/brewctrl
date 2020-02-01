import argparse
import os
from aiohttp import web

from ITempCtrl import ITempCtrl


class TempCtrlAPI:
    def __init__(self, tempctrl: ITempCtrl):
        assert isinstance(tempctrl, ITempCtrl)
        self.tempctrl = tempctrl

        self.app = web.Application()
        self.app.add_routes([
            web.get('/temperature', self.get_temperature),
            web.get('/setpoint', self.get_setpoint),
            web.post('/setpoint', self.set_setpoint)
        ])

    async def get_temperature(self, request):
        temperature = await self.tempctrl.get_temperature()
        return web.Response(body=str(temperature))

    async def get_setpoint(self, request):
        setpoint = await self.tempctrl.get_setpoint()
        return web.Response(body=str(setpoint))

    async def set_setpoint(self, request):
        setpoint = int(await request.text())
        await self.tempctrl.set_setpoint(setpoint)
        return web.Response()

    def start(self):
        web.run_app(self.app)
