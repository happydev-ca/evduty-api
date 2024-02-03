class TerminalResponse:
    def __init__(self, id="1", name="A", status="inUse", charge_box_identity="EVC30-12345", firmware_version="1.2.3"):
        self.id = id
        self.name = name
        self.status = status
        self.charge_box_identity = charge_box_identity
        self.firmware_version = firmware_version

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "status": self.status,
            "chargeBoxIdentity": self.charge_box_identity,
            "firmwareVersion": self.firmware_version
        }
