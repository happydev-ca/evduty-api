from evdutyapi import ChargingSession, ChargingStatus, NetworkInfo
from evdutyapi.charging_profile import ChargingProfile


class Terminal:
    def __init__(self, id: str, station_id: str, name: str, status: ChargingStatus, charge_box_identity: str, firmware_version: str, session: ChargingSession,
                 network_info: NetworkInfo = None,
                 charging_profile: ChargingProfile = None):
        self.id = id
        self.station_id = station_id
        self.name = name
        self.status = status
        self.charge_box_identity = charge_box_identity
        self.firmware_version = firmware_version
        self.session = session
        self.network_info = network_info
        self.charging_profile = charging_profile

    def __repr__(self) -> str:
        return f"<Terminal id:{self.id} station id:{self.station_id} name:{self.name} status:{self.status} charge_box_identity:{self.charge_box_identity} firmware_version={self.firmware_version}>"

    def __eq__(self, __value):
        return (self.id == __value.id and
                self.name == __value.name and
                self.status == __value.status and
                self.charge_box_identity == __value.charge_box_identity and
                self.firmware_version == __value.firmware_version and
                self.session == __value.session and
                self.network_info == __value.network_info and
                self.charging_profile == __value.charging_profile)
