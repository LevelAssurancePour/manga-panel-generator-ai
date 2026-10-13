"""Export service — PNG, CBZ, and layered PSD (via psd-tools) writers."""
from __future__ import annotations

import zipfile
from pathlib import Path

from manga_panel_generator.app.config import AppConfig


class ExportService:
    def __init__(self, cfg: AppConfig) -> None:
        self._cfg = cfg

    def to_cbz(self, page_paths: list[str], out_name: str) -> str:
        out = self._cfg.paths.exports_dir / f"{out_name}.cbz"
        with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as zf:
            for idx, p in enumerate(sorted(page_paths)):
                zf.write(p, arcname=f"{idx:03d}_{Path(p).name}")
        return str(out)

    def to_psd(self, panel_paths: list[str], out_name: str) -> str:
        from psd_tools import PSDImage  # type: ignore
        psd = PSDImage.new(mode="L", size=(2048, 2048))
        for idx, p in enumerate(panel_paths):
            layer = psd.create_pixel_layer(Image.open(p))
            layer.name = f"panel_{idx:02d}"
        out = self._cfg.paths.exports_dir / f"{out_name}.psd"
        psd.save(out)
        return str(out)