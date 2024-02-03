from datetime import datetime, timedelta

from evdutyapi import ChargingSession


class ChargingSessionResponse:
    def __init__(self, is_active, is_charging, volt, amp, power, energy_consumed, charge_start_date, duration):
        self.is_active = is_active
        self.is_charging = is_charging
        self.volt = volt
        self.amp = amp
        self.power = power
        self.energy_consumed = energy_consumed
        self.charge_start_date = charge_start_date
        self.duration = duration

    @classmethod
    def from_json(cls, data):
        return ChargingSession(is_active=data.get('isActive'),
                               is_charging=data.get('isCharging'),
                               volt=data.get('volt'),
                               amp=data.get('amp'),
                               power=data.get('power'),
                               energy_consumed=data.get('energyConsumed'),
                               start_date=datetime.fromtimestamp(data.get('chargeStartDate')),
                               duration=timedelta(seconds=data.get('duration')))

    def to_json(self):
        return {
            "isActive": self.is_active,
            "isCharging": self.is_charging,
            "volt": self.volt,
            "amp": self.amp,
            "power": self.power,
            "energyConsumed": self.energy_consumed,
            "chargeStartDate": self.charge_start_date,
            "duration": self.duration
        }

# costLocal: en cent (0.10039999999999999)
# pour estimated cost = 0.10039999999999999 * (energyConsumed)36459.92 / 1000 = 3.66$

# duration: int en seconds (76704.575 = 21:18:24 ==> new Date(76704575).toUTCString() = 21:18:24)
# chargeStartDate: int en seconds (1706973328 => 1706973328 * 1000 dans un new Date = Sat Feb 03 2024 10:15:28 GMT-0500)
