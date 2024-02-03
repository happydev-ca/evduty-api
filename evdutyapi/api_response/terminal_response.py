from evdutyapi import Terminal, Session, TerminalStatus


class TerminalResponse:
    def __init__(self, id, name, status, charge_box_identity, firmware_version):
        self.id = id
        self.name = name
        self.status = status
        self.charge_box_identity = charge_box_identity
        self.firmware_version = firmware_version

    @classmethod
    def from_json(cls, data):
        return Terminal(id=data.get('id'),
                        name=data.get('name'),
                        status=TerminalStatus(data.get('status')),
                        charge_box_identity=data.get('chargeBoxIdentity'),
                        firmware_version=data.get('firmwareVersion'),
                        session=Session.no_session())

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "status": self.status,
            "chargeBoxIdentity": self.charge_box_identity,
            "firmwareVersion": self.firmware_version
        }
