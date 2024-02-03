from evdutyapi import Terminal, ChargingStatus


class Station:
    def __init__(self, id: str, name: str, status: ChargingStatus, terminals: list[Terminal]):
        self.id = id
        self.name = name
        self.status = status
        self.terminals = terminals

    def __repr__(self):
        return f"<Station id:{self.id} name:{self.name} status:{self.status} terminals:{len(self.terminals)}>"

    def __eq__(self, __value):
        return (self.id == __value.id and
                self.name == __value.name and
                self.status == __value.status and
                self.terminals == __value.terminals)
