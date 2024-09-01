from typing import TypeAlias

Amp: TypeAlias = int


class ChargingProfile:
    def __init__(self, power_limitation: bool, current_limit: Amp, current_max: Amp):
        self.power_limitation = power_limitation
        self.current_limit = current_limit
        self.current_max = current_max

    def __repr__(self) -> str:
        return f"<ChargingProfile power_limitation:{self.power_limitation} current_limit:{self.current_limit} current_max:{self.current_max}>"

    def __eq__(self, __value):
        return (self.power_limitation == __value.power_limitation and
                self.current_limit == __value.current_limit and
                self.current_max == __value.current_max)
