"""Scans disk for SDXL / LoRA checkpoints and indexes them."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from manga_panel_generator.app.config import AppConfig


@dataclass(frozen=True)
class ModelEntry:
    name: str
    path: Path
    kind: str  # "sdxl" | "lora" | "vae"
    size_mb: int


class ModelRegistry:
    def __init__(self, cfg: AppConfig) -> None:
        self._cfg = cfg
        self._index: dict[str, ModelEntry] = {}

    def scan(self) -> None:
        root = self._cfg.paths.models_dir
        for path in root.rglob("*.safetensors"):
            kind = "lora" if "lora" in str(path).lower() else "sdxl"
            entry = ModelEntry(
                name=path.stem,
                path=path,
                kind=kind,
                size_mb=path.stat().st_size // (1024 * 1024),
            )
            self._index[entry.name] = entry

    def get(self, name: str) -> ModelEntry | None:
        return self._index.get(name)

    def count(self) -> int:
        return len(self._index)

    def all(self) -> list[ModelEntry]:
        return list(self._index.values())