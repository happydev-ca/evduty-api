from datetime import datetime, timedelta
from typing import Any, Dict
from zoneinfo import ZoneInfo
from .. import ChargingSession


class ChargingSessionResponse:

    @classmethod
    def from_json(cls, data: Dict[str, Any]) -> ChargingSession:
        return ChargingSession(is_active=data['isActive'],
                               is_charging=data['isCharging'],
                               volt=data['volt'],
                               amp=data['amp'],
                               power=data['power'],
                               energy_consumed=data['energyConsumed'],
                               start_date=datetime.fromtimestamp(data['chargeStartDate'], ZoneInfo('US/Eastern')),
                               duration=timedelta(seconds=data['duration']),
                               cost=ChargingSessionResponse.cost_from_json(data))

    @classmethod
    def cost_from_json(cls, data):
        return round((data['station']['terminal']['costLocal'] or 0) * data['energyConsumed'] / 1000, 2)
