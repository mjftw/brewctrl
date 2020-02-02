import asyncio
import json
from datetime import datetime
from aiohttp import web
from aiohttp_sse import sse_response, EventSourceResponse

from .interfaces import ITempCtrl
from .sse_helper import sse_packet


class TempCtrlAPI:
    def __init__(self, tempctrl: ITempCtrl):
        assert isinstance(tempctrl, ITempCtrl)
        self.tempctrl = tempctrl

        self.app = web.Application()
        self.app.add_routes([
            web.get('/temperature', self.get_temperature),
            web.get('/setpoint', self.get_setpoint),
            web.post('/setpoint', self.set_setpoint),
            web.get('/datastream', self.datastream),
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

    async def datastream(self, request):
        resp = EventSourceResponse(headers={'X-SSE': 'aiohttp_sse'})
        await resp.prepare(request)
        while True:
            temp = await self.tempctrl.get_temperature()
            data = {
                'temperature': temp,
                'time': datetime.now().isoformat()
            }
            await resp.send(data=json.dumps(data), event='data')
            await asyncio.sleep(1)
        resp.stop_streaming()
        await resp.wait()
        return resp

    async def _init_app(self):
        self._tempctrl_task = asyncio.ensure_future(self.tempctrl.start())
        return self.app

    def start(self):
        web.run_app(self._init_app())
