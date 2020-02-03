import asyncio
from asyncio import Queue
import json
from functools import wraps
from datetime import datetime
from aiohttp_sse import EventSourceResponse

from .interfaces import IEventStream


class SSEStream(IEventStream):
    def __init__(self):
        self._queue = Queue()

    async def put(self, event_name, data):
        assert isinstance(event_name, str)

        await self._queue.put((event_name, data))

    async def stream(self, request):
        response = EventSourceResponse(headers={'X-SSE': 'aiohttp_sse'})
        await response.prepare(request)

        while True:
            # Wait for a new event to send
            event = await self._queue.get()
            event_name = event[0]
            data = event[1]

            await response.send(
                data=json.dumps(data),
                event=event_name,
                id=datetime.now().isoformat())

        response.stop_streaming()
        await response.wait()
        return response



def datastream(event_name, co_func, period):
    @wraps(co_func)
    async def wrapped(request):
        response = EventSourceResponse(headers={'X-SSE': 'aiohttp_sse'})
        await response.prepare(request)
        while True:
            temp = await co_func()
            data = {
                'value': temp,
                'time': datetime.now().isoformat()
            }
            await response.send(data=json.dumps(data), event=event_name)
            await asyncio.sleep(period)
        response.stop_streaming()
        await response.wait()
        return response
    return  wrapped