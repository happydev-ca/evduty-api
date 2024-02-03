from enum import Enum

from evdutyapi import Terminal


class StationStatus(Enum):
    available = 'available'


class Station:
    def __init__(self, id: str, name: str, status: StationStatus, terminals: list[Terminal]):
        self.id = id
        self.name = name
        self.status = status
        self.terminals = terminals

    @classmethod
    def from_json(cls, data):
        return cls(id=data.get('id'),
                   name=data.get('name'),
                   status=StationStatus(data.get('status')),
                   terminals=[Terminal.from_json(t) for t in data.get('terminals')])

    def __repr__(self):
        return f"<Station id:{self.id} name:{self.name} status:{self.status} terminals:{len(self.terminals)}>"

    def __eq__(self, __value):
        return (self.id == __value.id and
                self.name == __value.name and
                self.status == __value.status and
                self.terminals == __value.terminals)