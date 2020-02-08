import json
from json.decoder import JSONDecodeError
from ast import literal_eval

from .interfaces import IConfig
from .interfaces.IConfig import MissingConfig


class JsonConfig(IConfig):
    ''' Horribly inefficient JSON backed config storage '''

    def __init__(self, filename: str):
        self.filename = filename

    async def write(self, name, value):
        if not isinstance(name, str):
            raise TypeError('name must be a string')

        # Check value is serialisable before continuing
        #   A TypeError or OverflowError will be raised if not
        json.dumps(value)

        try:
            with open(self.filename, 'r') as f:
                data = json.load(f)
        except FileNotFoundError:
            data = {}

        with open(self.filename, 'w') as f:
            data[name] = value
            json.dump(data, f)

    async def read(self, name):
        try:
            with open(self.filename, 'r') as f:
                data = json.load(f)
        except FileNotFoundError:
            return None

        if name not in data:
            raise MissingConfig(f'Config "{name}" not found in {self.filename}')

        return data[name]

    async def clear(self):
        with open(self.filename, 'w') as f:
            f.write('{}')