"""Thin handler for panel generation requests from the UI."""
from __future__ import annotations

import logging

from manga_panel_generator.core.panel_spec import PanelSpec
from manga_panel_generator.services.panel_pipeline import PanelPipeline

logger = logging.getLogger("mpg.handlers.panel")


class PanelHandler:
    """Translates UI events into pipeline calls. No business logic here."""

    def __init__(self, pipeline: PanelPipeline) -> None:
        self._pipeline = pipeline

    def generate(self, spec: PanelSpec) -> str:
        logger.info("generate panel_id=%s shot=%s", spec.panel_id, spec.shot.value)
        return self._pipeline.run_single(spec)

    def generate_batch(self, specs: list[PanelSpec]) -> list[str]:
        logger.info("generate_batch count=%d", len(specs))
        return self._pipeline.run_batch(specs)