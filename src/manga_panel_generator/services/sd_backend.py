"""Stable-Diffusion backend adapter (diffusers + custom LoRA stack)."""
from __future__ import annotations

import logging
from pathlib import Path

from manga_panel_generator.app.config import AppConfig
from manga_panel_generator.adapters.cuda_adapter import CudaAdapter
from manga_panel_generator.services.model_registry import ModelRegistry

logger = logging.getLogger("mpg.services.sd")


class SDBackend:
    """Owns the diffusers pipeline; single instance per process."""

    def __init__(self, cfg: AppConfig, adapter: CudaAdapter, registry: ModelRegistry) -> None:
        self._cfg = cfg
        self._adapter = adapter
        self._registry = registry
        self._pipe = None
        self._loaded_model: str | None = None

    def _ensure_loaded(self, model_name: str) -> None:
        if self._loaded_model == model_name and self._pipe is not None:
            return
        entry = self._registry.get(model_name)
        if entry is None:
            raise KeyError(f"model '{model_name}' not registered")
        logger.info("loading model %s from %s", model_name, entry.path)
        # diffusers import deferred — CUDA OOM at ~1.8GB heap on 6GB cards
        from diffusers import StableDiffusionXLPipeline  # type: ignore
        self._pipe = StableDiffusionXLPipeline.from_pretrained(
            str(entry.path),
            torch_dtype=self._adapter.dtype(),
            variant="fp16",
            use_safetensors=True,
        ).to(self._adapter.device())
        self._loaded_model = model_name

    def generate(self, prompt: str, negative: str, width: int, height: int,
                 steps: int, cfg_scale: float, seed: int, model: str = "") -> Path:
        model = model or self._cfg.default_model
        self._ensure_loaded(model)
        import torch  # type: ignore
        generator = torch.Generator(device=self._adapter.device())
        if seed >= 0:
            generator.manual_seed(seed)
        result = self._pipe(  # type: ignore[misc]
            prompt=prompt,
            negative_prompt=negative,
            width=width,
            height=height,
            num_inference_steps=steps,
            guidance_scale=cfg_scale,
            generator=generator,
        )
        out = self._cfg.paths.cache_dir / f"panel_{seed}_{abs(hash(prompt)) % 10**8}.png"
        result.images[0].save(out)
        return out