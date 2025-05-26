from typing import Self

class ChargingSessionResponseBuilder:
    def __init__(self):
        self._data = {
            'isActive': True,
            'isCharging': True,
            'volt': 240,
            'amp': 13.9,
            'power': 3336,
            'energyConsumed': 36459.92,
            'chargeStartDate': 1706897191,
            'duration': 77602.7,
            'station': {
                'terminal': {
                    'costLocal': 0.10039
                }
            }
        }

    @classmethod
    def default(cls) -> Self:
        return cls()

    def with_cost(self, cost: float | None) -> Self:
        self._data['station']['terminal']['costLocal'] = cost
        return self

    def build(self) -> dict:
        return self._data
