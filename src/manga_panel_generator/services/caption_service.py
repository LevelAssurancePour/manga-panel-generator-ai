"""Prompt enrichment — injects manga-specific descriptors and shot grammar."""
from __future__ import annotations

from manga_panel_generator.app.config import AppConfig
from manga_panel_generator.core.panel_spec import ShotType, ToneMark

_SHOT_PREFIX = {
    ShotType.WIDE: "wide establishing shot, full environment visible,",
    ShotType.MEDIUM: "medium shot, waist-up composition,",
    ShotType.CLOSE_UP: "close-up, emotional focus on face,",
    ShotType.EXTREME_CLOSE_UP: "extreme close-up, single eye detail,",
    ShotType.OVER_SHOULDER: "over-the-shoulder framing, depth on foreground,",
}

_TONE_SUFFIX = {
    ToneMark.SPARKLE: "sparkle overlay, shoujo screentone, glossy highlights,",
    ToneMark.SWEAT: "sweat drop glyph, comedic tension lines,",
    ToneMark.ANGER_VEIN: "cross-popping anger vein, red screentone,",
    ToneMark.SPEED_LINES: "radial speed lines, motion blur streaks,",
    ToneMark.NONE: "",
}

_STYLE_LOCK = (
    "monochrome manga panel, clean ink linework, screentone shading, "
    "high contrast, printed tankobon quality, no color, "
)


class CaptionService:
    def __init__(self, cfg: AppConfig) -> None:
        self._cfg = cfg

    def enrich(self, prompt: str, shot: ShotType, tone: ToneMark) -> str:
        parts = [_SHOT_PREFIX[shot], _STYLE_LOCK, prompt.strip()]
        if _TONE_SUFFIX[tone]:
            parts.append(_TONE_SUFFIX[tone])
        return " ".join(p for p in parts if p)