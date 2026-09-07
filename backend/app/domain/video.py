import os
from typing import Self
from dataclasses import dataclass, asdict

@dataclass
class Video:
    id: str
    name: str
    filename: str
    path: str
    thumbnail: str | None = None
    duration: float | None = None

    def exists(self) -> bool:
        return os.path.exists(self.path)

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        return cls(**data)

    def to_dict(self) -> dict:
        return asdict(self)