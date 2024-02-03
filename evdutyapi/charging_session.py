from datetime import datetime, timedelta
from typing import TypeAlias

Volt: TypeAlias = float
Amp: TypeAlias = float
Watt: TypeAlias = float
Wh: TypeAlias = float
Dollar: TypeAlias = float


class ChargingSession:
    def __init__(self, is_active: bool, is_charging: bool, volt: Volt, amp: Amp, power: Watt, energy_consumed: Wh, start_date: datetime, duration: timedelta, cost: Dollar):
        self.is_active = is_active
        self.is_charging = is_charging
        self.volt = volt
        self.amp = amp
        self.power = power
        self.energy_consumed = energy_consumed
        self.start_date = start_date
        self.duration = duration
        self.cost = cost

    def __repr__(self):
        return (f"<ChargingSession is_active:{self.is_active} "
                f"is_charging={self.is_charging} "
                f"volt={self.volt}V amp={self.amp}A "
                f"power={self.power}Wh "
                f"energy_consumed={self.energy_consumed}Wh "
                f"start_date={self.start_date} "
                f"duration={self.duration} "
                f"cost={self.cost}$>")

    def __eq__(self, __value):
        return (self.is_active == __value.is_active and
                self.is_charging == __value.is_charging and
                self.volt == __value.volt and
                self.amp == __value.amp and
                self.power == __value.power and
                self.energy_consumed == __value.energy_consumed and
                self.start_date == __value.start_date and
                self.duration == __value.duration and
                self.cost == __value.cost)

    @classmethod
    def no_session(cls):
        return cls(is_active=False,
                   is_charging=False,
                   volt=0,
                   amp=0,
                   power=0,
                   energy_consumed=0,
                   start_date=datetime.min,
                   duration=timedelta(seconds=0),
                   cost=0)
