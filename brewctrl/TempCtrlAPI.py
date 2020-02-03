import asyncio
import json
from datetime import datetime
from aiohttp import web
from aiohttp_sse import sse_response, EventSourceResponse

from .interfaces import ITempCtrl
from .SSEStream import SSEStream


class TempCtrlAPI:
    def __init__(self, tempctrl: ITempCtrl, event_stream: SSEStream):
        assert isinstance(tempctrl, ITempCtrl)
        assert isinstance(event_stream, SSEStream)

        self.tempctrl = tempctrl

        self.app = web.Application()
        self.app.add_routes([
            web.get('/temperature', self.get_temperature),
            web.get('/setpoint', self.get_setpoint),
            web.post('/setpoint', self.set_setpoint),
            web.get('/tolerance', self.get_tolerance),
            web.post('/tolerance', self.set_tolerance),
            web.get('/datastream', event_stream.stream),
        ])

        self._tempctrl_task = None

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

    async def get_tolerance(self, request):
        tolerance = await self.tempctrl.get_tolerance()
        return web.Response(body=str(tolerance))

    async def set_tolerance(self, request):
        tolerance = int(await request.text())
        await self.tempctrl.set_tolerance(tolerance)
        return web.Response()

    async def _init_app(self):
        self._tempctrl_task = asyncio.ensure_future(self.tempctrl.start())
        return self.app

    def start(self):
        web.run_app(self._init_app())
