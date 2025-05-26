from typing import Any, Dict


class MaxChargingCurrentRequest:

    @classmethod
    def from_terminal_response(cls, data: Dict[str, Any], current) -> Dict[str, Any]:
        request = data.copy()
        request.pop('cost', None)
        request.pop('alternateCost', None)
        request.pop('sessionTimeLimits', None)
        if request.get('costLocal') is None:
            request.pop('costLocal', None)
        request['chargingProfile'] = {'chargingRate': current, 'chargingRateUnit': 'A'}
        return request