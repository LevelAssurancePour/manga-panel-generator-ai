"""Platform adapter — CUDA / ROCm / CPU device selection."""
from __future__ import annotations

import logging

from manga_panel_generator.app.config import AppConfig

logger = logging.getLogger("mpg.adapters.cuda")


class CudaAdapter:
    def __init__(self, cfg: AppConfig) -> None:
        self._cfg = cfg
        self._device = "cpu"
        self._torch = None

    def probe(self) -> str:
        try:
            import torch  # type: ignore
            self._torch = torch
            if self._cfg.device == "cuda" and torch.cuda.is_available():
                self._device = "cuda"
            elif self._cfg.device == "rocm" and hasattr(torch, "hip"):
                self._device = "cuda"
            else:
                self._device = "cpu"
        except ImportError:
            logger.warning("torch not available — falling back to CPU")
            self._device = "cpu"
        logger.info("device resolved: %s", self._device)
        return self._device

    def device(self) -> str:
        return self._device

    def dtype(self):
        if self._torch is None:
            return None
        return self._torch.float16 if self._device == "cuda" else self._torch.float32