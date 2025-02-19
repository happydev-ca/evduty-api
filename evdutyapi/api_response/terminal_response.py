from dataclasses import dataclass
from typing import Any, Dict
from evdutyapi import Terminal, ChargingSession, ChargingStatus


@dataclass(frozen=True)
class TerminalResponse:
    id: str
    name: str
    status: str
    charge_box_identity: str
    firmware_version: str

    @classmethod
    def from_json(cls, data: Dict[str, Any], station_id: str) -> Terminal:
        return Terminal(id=data['id'],
                        station_id=station_id,
                        name=data['name'],
                        status=ChargingStatus(data['status']),
                        charge_box_identity=data['chargeBoxIdentity'],
                        firmware_version=data['firmwareVersion'],
                        session=ChargingSession.no_session())

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "status": self.status,
            "chargeBoxIdentity": self.charge_box_identity,
            "firmwareVersion": self.firmware_version
        }
