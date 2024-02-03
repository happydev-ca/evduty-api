class StationResponse:
    def __init__(self, id="1", name="A", status="available", terminals=None):
        if terminals is None:
            terminals = []
        self.id = id
        self.name = name
        self.status = status
        self.terminals = terminals

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "status": self.status,
            "terminals": self.terminals
        }
