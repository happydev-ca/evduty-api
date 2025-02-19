from dataclasses import dataclass
from evdutyapi import ChargingSession, ChargingStatus, NetworkInfo
from evdutyapi.charging_profile import ChargingProfile


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
