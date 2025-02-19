from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import TypeAlias, Self

Volt: TypeAlias = float
Amp: TypeAlias = float
Watt: TypeAlias = float
Wh: TypeAlias = float
Dollar: TypeAlias = float


@dataclass(frozen=True)
class ChargingSession:
    is_active: bool
    is_charging: bool
    volt: Volt
    amp: Amp
    power: Watt
    energy_consumed: Wh
    start_date: datetime
    duration: timedelta
    cost: Dollar

    @classmethod
    def no_session(cls) -> Self:
        return cls(
            is_active=False,
            is_charging=False,
            volt=0,
            amp=0,
            power=0,
            energy_consumed=0,
            start_date=datetime.min,
            duration=timedelta(seconds=0),
            cost=0
        )
