from typing import Dict, Any
from evdutyapi import Station
from evdutyapi.api_response.terminal_response import TerminalResponse


class StationResponse:
    def __init__(self, id, name, terminals):
        if terminals is None:
            terminals = []
        self.id = id
        self.name = name
        self.terminals = terminals

    @classmethod
    def from_json(cls, data: Dict[str, Any]) -> Station:
        return Station(id=data['id'],
                       name=data['name'],
                       terminals=[TerminalResponse.from_json(t, data['id']) for t in data['terminals']])

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "terminals": self.terminals
        }
