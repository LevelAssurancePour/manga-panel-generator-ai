"""Splits a manga page into panel bounding boxes (right-to-left reading)."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class BBox:
    x: int
    y: int
    w: int
    h: int


@dataclass(frozen=True)
class PageTemplate:
    name: str
    columns: int
    rows: int
    gutter: int
    reading_direction: str = "rtl"


TEMPLATES = {
    "yonkoma": PageTemplate(name="yonkoma", columns=1, rows=4, gutter=18),
    "kishotenketsu": PageTemplate(name="kishotenketsu", columns=2, rows=3, gutter=24),
    "action_split": PageTemplate(name="action_split", columns=2, rows=2, gutter=14),
    "splash": PageTemplate(name="splash", columns=1, rows=1, gutter=0),
}


def compute_bboxes(template: PageTemplate, page_w: int, page_h: int) -> list[BBox]:
    """Return bboxes ordered for right-to-left, top-to-bottom reading."""
    inner_w = page_w - template.gutter * (template.columns + 1)
    inner_h = page_h - template.gutter * (template.rows + 1)
    cell_w = inner_w // template.columns
    cell_h = inner_h // template.rows

    boxes: list[BBox] = []
    for row in range(template.rows):
        col_order = range(template.columns) if template.reading_direction == "ltr" else \
            reversed(range(template.columns))
        for col in col_order:
            x = template.gutter + col * (cell_w + template.gutter)
            y = template.gutter + row * (cell_h + template.gutter)
            boxes.append(BBox(x=x, y=y, w=cell_w, h=cell_h))
    return boxes