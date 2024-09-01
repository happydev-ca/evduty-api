from typing import TypeAlias

Amp: TypeAlias = int


class ChargingProfile:
    def __init__(self, power_limitation: bool, current_limit: Amp):
        self.power_limitation = power_limitation
        self.current_limit = current_limit

    def __repr__(self) -> str:
        return f"<ChargingProfile power_limitation:{self.power_limitation} current_limit:{self.current_limit}>"

    def __eq__(self, __value):
        return (self.power_limitation == __value.power_limitation and
                self.current_limit == __value.current_limit)
