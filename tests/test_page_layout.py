"""Tests for RTL panel bounding-box computation."""
from manga_panel_generator.core.page_layout import TEMPLATES, compute_bboxes


def test_yonkoma_has_four_boxes():
    boxes = compute_bboxes(TEMPLATES["yonkoma"], 1024, 2048)
    assert len(boxes) == 4


def test_rtl_order_first_box_is_rightmost():
    boxes = compute_bboxes(TEMPLATES["kishotenketsu"], 2048, 2048)
    assert boxes[0].x > boxes[1].x


def test_boxes_do_not_overlap():
    boxes = compute_bboxes(TEMPLATES["action_split"], 2048, 2048)
    for i, a in enumerate(boxes):
        for b in boxes[i + 1:]:
            assert a.x + a.w <= b.x or b.x + b.w <= a.x or a.y + a.h <= b.y or b.y + b.h <= a.y