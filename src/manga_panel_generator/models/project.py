"""Project model — a storyboard of pages, each with ordered panels."""
from __future__ import annotations

from dataclasses import dataclass, field

from manga_panel_generator.core.panel_spec import PanelSpec
from manga_panel_generator.models.character import Character


@dataclass
class PageModel:
    index: int
    template: str
    panels: list[PanelSpec] = field(default_factory=list)


@dataclass
class Project:
    title: str
    author: str
    characters: list[Character] = field(default_factory=list)
    pages: list[PageModel] = field(default_factory=list)
    schema_version: int = 3

    def add_page(self, template: str) -> PageModel:
        page = PageModel(index=len(self.pages), template=template)
        self.pages.append(page)
        return page