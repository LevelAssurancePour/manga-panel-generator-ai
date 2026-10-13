"""Composes generated panels into a full page with gutters and bubbles."""
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw

from manga_panel_generator.app.config import AppConfig
from manga_panel_generator.core.page_layout import BBox, PageTemplate, TEMPLATES


class PageComposer:
    def __init__(self, cfg: AppConfig) -> None:
        self._cfg = cfg

    @staticmethod
    def templates() -> dict[str, PageTemplate]:
        return TEMPLATES

    def compose(self, template: PageTemplate, boxes: list[BBox], panel_paths: list[str]) -> str:
        page_w = self._cfg.max_panel_width
        page_h = self._cfg.max_panel_height
        canvas = Image.new("L", (page_w, page_h), 255)
        draw = ImageDraw.Draw(canvas)

        for box, path in zip(boxes, panel_paths):
            panel = Image.open(path).convert("L").resize((box.w, box.h))
            canvas.paste(panel, (box.x, box.y))
            draw.rectangle([box.x, box.y, box.x + box.w, box.y + box.h], outline=0, width=3)

        out = self._cfg.paths.exports_dir / f"page_{template.name}.png"
        canvas.save(out, dpi=(300, 300))
        return str(out)