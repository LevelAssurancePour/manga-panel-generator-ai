"""Character sheet model — persisted per-project."""
from __future__ import annotations

from dataclasses import dataclass, field, asdict
import json


@dataclass
class Character:
    name: str
    hair: str = ""
    eyes: str = ""
    outfit: str = ""
    age_range: str = ""
    lora_trigger: str = ""
    tags: list[str] = field(default_factory=list)

    def to_json(self) -> str:
        return json.dumps(asdict(self), ensure_ascii=False, indent=2)

    @classmethod
    def from_json(cls, raw: str) -> "Character":
        return cls(**json.loads(raw))