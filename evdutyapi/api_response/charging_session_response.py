from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from evdutyapi import ChargingSession


class ChargingSessionResponse:
    def __init__(self, is_active, is_charging, volt, amp, power, energy_consumed, charge_start_date, duration, cost_local):
        self.is_active = is_active
        self.is_charging = is_charging
        self.volt = volt
        self.amp = amp
        self.power = power
        self.energy_consumed = energy_consumed
        self.charge_start_date = charge_start_date
        self.duration = duration
        self.cost_local = cost_local

    @classmethod
    def from_json(cls, data):
        return ChargingSession(is_active=data['isActive'],
                               is_charging=data['isCharging'],
                               volt=data['volt'],
                               amp=data['amp'],
                               power=data['power'],
                               energy_consumed=data['energyConsumed'],
                               start_date=datetime.fromtimestamp(data['chargeStartDate'], ZoneInfo('US/Eastern')),
                               duration=timedelta(seconds=data['duration']),
                               cost=round(data['station']['terminal']['costLocal'] * data['energyConsumed'] / 1000, 2))

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
