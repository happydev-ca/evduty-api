from evdutyapi import Terminal, ChargingSession, ChargingStatus


class TerminalResponse:
    def __init__(self, id, name, status, charge_box_identity, firmware_version):
        self.id = id
        self.name = name
        self.status = status
        self.charge_box_identity = charge_box_identity
        self.firmware_version = firmware_version

    @classmethod
    def from_json(cls, data):
        return Terminal(id=data['id'],
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
