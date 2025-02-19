from dataclasses import dataclass, field
from typing import Dict, Any, List
from evdutyapi import Station
from evdutyapi.api_response.terminal_response import TerminalResponse


@dataclass(frozen=True)
class StationResponse:
    id: str
    name: str
    terminals: List[Dict[str, Any]] = field(default_factory=list)

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
