from evdutyapi import Terminal


class Station:
    def __init__(self, id: str, name: str, terminals: list[Terminal]):
        self.id = id
        self.name = name
        self.terminals = terminals

    def __repr__(self) -> str:
        return f"<Station id:{self.id} name:{self.name} terminals:{len(self.terminals)}>"

    def __eq__(self, __value):
        return (self.id == __value.id and
                self.name == __value.name and
                self.terminals == __value.terminals)
