"""Handler for whole-page composition requests."""
from __future__ import annotations

from manga_panel_generator.core.page_layout import PageTemplate, compute_bboxes
from manga_panel_generator.services.page_composer import PageComposer


class PageHandler:
    def __init__(self, composer: PageComposer) -> None:
        self._composer = composer

    def compose(self, template_name: str, page_w: int, page_h: int, panel_paths: list[str]) -> str:
        template = PageComposer.templates()[template_name]
        boxes = compute_bboxes(template, page_w, page_h)
        return self._composer.compose(template, boxes, panel_paths)