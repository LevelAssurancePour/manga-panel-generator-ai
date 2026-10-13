"""Bubble placement heuristics for manga dialogue and SFX."""
from __future__ import annotations

from dataclasses import dataclass

from manga_panel_generator.core.page_layout import BBox


@dataclass(frozen=True)
class Bubble:
    text: str
    bbox: BBox
    tail_x: int
    tail_y: int
    style: str = "speech"  # speech | thought | narration | sfx


def place_bubble(panel: BBox, text: str, style: str, anchor: str = "tl") -> Bubble:
    w = max(90, int(len(text) * 11))
    h = max(48, int(len(text) * 0.8) + 24)
    anchors = {
        "tl": (panel.x + 12, panel.y + 12),
        "tr": (panel.x + panel.w - w - 12, panel.y + 12),
        "bl": (panel.x + 12, panel.y + panel.h - h - 12),
        "br": (panel.x + panel.w - w - 12, panel.y + panel.h - h - 12),
    }
    bx, by = anchors.get(anchor, anchors["tl"])
    tail_x = bx + w // 2
    tail_y = by + h if by < panel.y + panel.h // 2 else by
    return Bubble(text=text, bbox=BBox(bx, by, w, h), tail_x=tail_x, tail_y=tail_y, style=style)