"""Screentone / halftone helpers applied post-generation."""
from __future__ import annotations

from PIL import Image, ImageOps


def apply_halftone(img: Image.Image, dot_size: int = 4) -> Image.Image:
    gray = ImageOps.grayscale(img)
    small = gray.resize((gray.width // dot_size, gray.height // dot_size), Image.BILINEAR)
    quantized = small.point(lambda v: 0 if v < 128 else 255, mode="1")
    return quantized.convert("L").resize(gray.size, Image.NEAREST)


def apply_speed_lines(img: Image.Image, cx: int, cy: int, count: int = 96) -> Image.Image:
    from PIL import ImageDraw
    out = img.copy()
    draw = ImageDraw.Draw(out)
    import math
    for i in range(count):
        angle = (2 * math.pi / count) * i
        x2 = cx + int(math.cos(angle) * max(img.size))
        y2 = cy + int(math.sin(angle) * max(img.size))
        draw.line([cx, cy, x2, y2], fill=0, width=1)
    return out