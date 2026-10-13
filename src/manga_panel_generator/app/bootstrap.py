"""Bootstrap wires services together and warms the runtime up."""
from __future__ import annotations

import logging
from dataclasses import dataclass, field

from manga_panel_generator.app.config import AppConfig
from manga_panel_generator.services.model_registry import ModelRegistry
from manga_panel_generator.services.panel_pipeline import PanelPipeline
from manga_panel_generator.services.sd_backend import SDBackend
from manga_panel_generator.services.caption_service import CaptionService
from manga_panel_generator.services.export_service import ExportService
from manga_panel_generator.adapters.cuda_adapter import CudaAdapter

logger = logging.getLogger("mpg.bootstrap")


@dataclass
class Services:
    registry: ModelRegistry
    backend: SDBackend
    captions: CaptionService
    pipeline: PanelPipeline
    exporter: ExportService


@dataclass
class Bootstrap:
    cfg: AppConfig
    fatal_error: str | None = None
    services: Services | None = None
    _extra: dict = field(default_factory=dict)

    def warm_up(self) -> None:
        try:
            adapter = CudaAdapter(cfg=self.cfg)
            adapter.probe()

            registry = ModelRegistry(cfg=self.cfg)
            registry.scan()

            backend = SDBackend(cfg=self.cfg, adapter=adapter, registry=registry)
            captions = CaptionService(cfg=self.cfg)
            pipeline = PanelPipeline(cfg=self.cfg, backend=backend, captions=captions)
            exporter = ExportService(cfg=self.cfg)

            self.services = Services(
                registry=registry,
                backend=backend,
                captions=captions,
                pipeline=pipeline,
                exporter=exporter,
            )
            logger.info("Bootstrap OK — %d models registered", registry.count())
        except Exception as exc:  # noqa: BLE001 — top-level boot guard
            logger.exception("Bootstrap crashed")
            self.fatal_error = str(exc)