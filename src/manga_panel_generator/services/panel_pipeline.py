"""Panel pipeline — orchestrates caption enrichment + generation."""
from __future__ import annotations

import logging

from manga_panel_generator.app.config import AppConfig
from manga_panel_generator.core.panel_spec import PanelSpec
from manga_panel_generator.services.caption_service import CaptionService
from manga_panel_generator.services.sd_backend import SDBackend
from manga_panel_generator.utils.cache import DiskCache

logger = logging.getLogger("mpg.services.pipeline")


class PanelPipeline:
    def __init__(self, cfg: AppConfig, backend: SDBackend, captions: CaptionService) -> None:
        self._cfg = cfg
        self._backend = backend
        self._captions = captions
        self._cache = DiskCache(cfg.paths.cache_dir / "panels")

    def run_single(self, spec: PanelSpec) -> str:
        key = spec.cache_key()
        cached = self._cache.get(key)
        if cached is not None:
            logger.debug("cache hit panel_id=%s", spec.panel_id)
            return str(cached)

        enriched = self._captions.enrich(spec.prompt, spec.shot, spec.tone)
        out = self._backend.generate(
            prompt=enriched,
            negative=spec.negative_prompt,
            width=spec.width,
            height=spec.height,
            steps=spec.steps,
            cfg_scale=spec.cfg_scale,
            seed=spec.seed,
        )
        self._cache.put(key, out)
        return str(out)

    def run_batch(self, specs: list[PanelSpec]) -> list[str]:
        return [self.run_single(s) for s in specs]