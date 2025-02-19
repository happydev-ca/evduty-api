from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Any, Dict
from zoneinfo import ZoneInfo
from evdutyapi import ChargingSession


@dataclass(frozen=True)
class ChargingSessionResponse:
    is_active: bool
    is_charging: bool
    volt: float
    amp: float
    power: float
    energy_consumed: float
    charge_start_date: int  # Unix timestamp
    duration: float  # seconds
    cost_local: float | None

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
                               cost=round((data['station']['terminal']['costLocal'] or 0) * data['energyConsumed'] / 1000, 2))

    def to_json(self):
        return {
            "isActive": self.is_active,
            "isCharging": self.is_charging,
            "volt": self.volt,
            "amp": self.amp,
            "power": self.power,
            "energyConsumed": self.energy_consumed,
            "chargeStartDate": self.charge_start_date,
            "duration": self.duration,
            "station": {
                "terminal": {
                    "costLocal": self.cost_local
                }
            }
        }
