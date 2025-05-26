from typing import Self


class StationResponseBuilder:
    def __init__(self):
        self._data = {
            'id': 'station_id',
            'name': 'station_name',
            'terminals': [
                {
                    'id': 'terminal_id',
                    'name': 'terminal_name',
                    'status': 'inUse',
                    'chargeBoxIdentity': 'identity',
                    'firmwareVersion': 'version'
                }
            ]
        }

    @classmethod
    def default(cls) -> Self:
        return cls()

    def build(self) -> dict:
        return self._data
