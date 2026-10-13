"""PanelSpec — the canonical description of one manga panel."""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Sequence


class ShotType(str, Enum):
    WIDE = "wide"
    MEDIUM = "medium"
    CLOSE_UP = "close_up"
    EXTREME_CLOSE_UP = "extreme_close_up"
    OVER_SHOULDER = "over_shoulder"


class ToneMark(str, Enum):
    SPARKLE = "sparkle"
    SWEAT = "sweat"
    ANGER_VEIN = "anger_vein"
    SPEED_LINES = "speed_lines"
    NONE = "none"


@dataclass(frozen=True)
class PanelSpec:
    panel_id: str
    prompt: str
    negative_prompt: str
    shot: ShotType
    tone: ToneMark
    width: int = 1024
    height: int = 1024
    seed: int = -1
    steps: int = 28
    cfg_scale: float = 6.5
    characters: Sequence[str] = field(default_factory=tuple)
    locale: str = "ja"

    def cache_key(self) -> str:
        return (
            f"{self.prompt}|{self.negative_prompt}|{self.shot.value}|"
            f"{self.tone.value}|{self.width}x{self.height}|{self.seed}|"
            f"{self.steps}|{self.cfg_scale}|{','.join(self.characters)}"
        )