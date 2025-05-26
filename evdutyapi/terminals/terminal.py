from dataclasses import dataclass
from enum import Enum
from typing import TypeAlias

from .. import ChargingSession

Amp: TypeAlias = int


class ChargingStatus(Enum):
    available = 'available'
    in_use = 'inUse'
    out_of_service = 'outOfService'


@dataclass(frozen=True)
class NetworkInfo:
    wifi_ssid: str
    wifi_rssi: int
    mac_address: str
    ip_address: str


@dataclass(frozen=True)
class ChargingProfile:
    power_limitation: bool
    current_limit: Amp
    current_max: Amp


@dataclass
class Terminal:
    id: str
    station_id: str
    name: str
    status: ChargingStatus
    charge_box_identity: str
    firmware_version: str
    session: ChargingSession
    network_info: NetworkInfo | None = None
    charging_profile: ChargingProfile | None = None
