import json
from json.decoder import JSONDecodeError

from .interfaces import IStorage


class JsonStorage(IStorage):
    ''' Horribly inefficient JSON backed storage '''

    def __init__(self, filename: str):
        self.filename = filename

    async def write_int(self, name, value):
        try:
            with open(self.filename, 'r') as f:
                data = json.load(f)
        except FileNotFoundError:
            data = {}

        with open(self.filename, 'w') as f:
            data[name] = int(value)
            json.dump(data, f)

    async def read_int(self, name):
        try:
            with open(self.filename, 'r') as f:
                data = json.load(f)
        except FileNotFoundError:
            return None

        return None if name not in data else data[name]