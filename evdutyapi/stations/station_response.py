from typing import Dict, Any
from .. import ChargingSession, ChargingStatus, Station, Terminal


class StationResponse:

    @classmethod
    def from_json(cls, data: Dict[str, Any]) -> Station:
        return Station(id=data['id'],
                       name=data['name'],
                       terminals=[StationResponse.terminal_from_json(t, data['id']) for t in data['terminals']])

    @classmethod
    def terminal_from_json(cls, data: Dict[str, Any], station_id: str) -> Terminal:
        return Terminal(id=data['id'],
                        station_id=station_id,
                        name=data['name'],
                        status=ChargingStatus(data['status']),
                        charge_box_identity=data['chargeBoxIdentity'],
                        firmware_version=data['firmwareVersion'],
                        session=ChargingSession.no_session())
