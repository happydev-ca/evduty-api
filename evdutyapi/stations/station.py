from dataclasses import dataclass
from evdutyapi import Terminal


@dataclass(frozen=True)
class Station:
    id: str
    name: str
    terminals: list[Terminal]
