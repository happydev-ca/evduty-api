from evdutyapi import ChargingSession, ChargingStatus


class Terminal:
    def __init__(self, id: str, name: str, status: ChargingStatus, charge_box_identity: str, firmware_version: str, session: ChargingSession):
        self.id = id
        self.name = name
        self.status = status
        self.charge_box_identity = charge_box_identity
        self.firmware_version = firmware_version
        self.session = session

    def __repr__(self):
        return f"<Terminal id:{self.id} name:{self.name} status:{self.status} charge_box_identity:{self.charge_box_identity} firmware_version={self.firmware_version}>"

    def __eq__(self, __value):
        return (self.id == __value.id and
                self.name == __value.name and
                self.status == __value.status and
                self.charge_box_identity == __value.charge_box_identity and
                self.firmware_version == __value.firmware_version)
