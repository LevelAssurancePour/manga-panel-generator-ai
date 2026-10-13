"""Application configuration loaded from TOML + env overrides."""
from __future__ import annotations

import os
import tomllib
from dataclasses import dataclass, field
from pathlib import Path


@dataclass(frozen=True)
class Paths:
    root: Path
    models_dir: Path
    cache_dir: Path
    log_dir: Path
    exports_dir: Path


@dataclass(frozen=True)
class AppConfig:
    version: str
    log_level: str
    default_model: str
    device: str
    max_panel_width: int
    max_panel_height: int
    paths: Paths
    extra: dict = field(default_factory=dict)

    @classmethod
    def load(cls, config_path: Path | None = None) -> "AppConfig":
        root = Path(os.environ.get("MPG_HOME", Path.home() / ".manga-panel-generator-ai"))
        cfg_file = config_path or root / "config.toml"
        raw: dict = {}
        if cfg_file.exists():
            with cfg_file.open("rb") as fh:
                raw = tomllib.load(fh)

        paths = Paths(
            root=root,
            models_dir=root / "models",
            cache_dir=root / "cache",
            log_dir=root / "logs",
            exports_dir=root / "exports",
        )
        for p in (paths.models_dir, paths.cache_dir, paths.log_dir, paths.exports_dir):
            p.mkdir(parents=True, exist_ok=True)

        return cls(
            version=raw.get("version", "0.6.3"),
            log_level=os.environ.get("MPG_LOG_LEVEL", raw.get("log_level", "INFO")),
            default_model=raw.get("default_model", "koharu-sdxl-manga-v3"),
            device=os.environ.get("MPG_DEVICE", raw.get("device", "cuda")),
            max_panel_width=int(raw.get("max_panel_width", 2048)),
            max_panel_height=int(raw.get("max_panel_height", 2048)),
            paths=paths,
            extra=raw.get("extra", {}),
        )