from enum import Enum


class ChargingStatus(Enum):
    available = 'available'
    in_use = 'inUse'
    out_of_service = 'outOfService'
