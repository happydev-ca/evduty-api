from typing import Self


class TerminalResponseBuilder:
    def __init__(self):
        self._data = {
            'wifiSSID': 'wifi',
            'wifiRSSI': -66,
            'macAddress': '11:22:33:44:AA:BB',
            'localIPAddress': '192.168.1.5',
            'amperage': 30,
            'chargingProfile': {
                'chargingRate': 15
            },
            'cost': 'any',
            'alternateCost': 'any',
            'sessionTimeLimits': 'any',
            'costLocal': 0.1234
        }

    @classmethod
    def default(cls) -> Self:
        return cls()

    def without_charging_profile(self):
        self._data.pop('chargingProfile', None)
        return self

    def with_charging_rate(self, current_limit: int) -> Self:
        self._data['chargingProfile']['chargingRate'] = current_limit
        return self

    def with_amperage(self, current_max: int) -> Self:
        self._data['amperage'] = current_max
        return self

    def with_cost_local(self, cost: float | None) -> Self:
        self._data['costLocal'] = cost
        return self

    def build(self) -> dict:
        return self._data