from enum import Enum


class TerminalStatus(Enum):
    available = 'available'
    in_use = 'inUse'


class Terminal:
    def __init__(self, id: str, name: str, status: TerminalStatus, charge_box_identity: str, firmware_version: str):
        self.id = id
        self.name = name
        self.status = status
        self.charge_box_identity = charge_box_identity
        self.firmware_version = firmware_version

    @classmethod
    def from_json(cls, data):
        return cls(id=data.get('id'),
                   name=data.get('name'),
                   status=TerminalStatus(data.get('status')),
                   charge_box_identity=data.get('chargeBoxIdentity'),
                   firmware_version=data.get('firmwareVersion'))

    def __repr__(self):
        return f"<Terminal id:{self.id} name:{self.name} status:{self.status} charge_box_identity:{self.charge_box_identity} firmware_version={self.firmware_version}>"

    def __eq__(self, __value):
        return (self.id == __value.id and
                self.name == __value.name and
                self.status == __value.status and
                self.charge_box_identity == __value.charge_box_identity and
                self.firmware_version == __value.firmware_version)
