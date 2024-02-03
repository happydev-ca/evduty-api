from evdutyapi import Station, ChargingStatus
from evdutyapi.api_response.terminal_response import TerminalResponse


class StationResponse:
    def __init__(self, id, name, status, terminals):
        if terminals is None:
            terminals = []
        self.id = id
        self.name = name
        self.status = status
        self.terminals = terminals

    @classmethod
    def from_json(cls, data):
        return Station(id=data['id'],
                       name=data['name'],
                       status=ChargingStatus(data['status']),
                       terminals=[TerminalResponse.from_json(t) for t in data['terminals']])

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "status": self.status,
            "terminals": self.terminals
        }
