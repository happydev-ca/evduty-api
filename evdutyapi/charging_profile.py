from dataclasses import dataclass
from typing import TypeAlias

Amp: TypeAlias = int


@dataclass(frozen=True)
class ChargingProfile:
    power_limitation: bool
    current_limit: Amp
    current_max: Amp
