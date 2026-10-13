"""Small content-addressed disk cache for generated panels."""
from __future__ import annotations

import hashlib
from pathlib import Path


class DiskCache:
    def __init__(self, root: Path) -> None:
        self._root = root
        self._root.mkdir(parents=True, exist_ok=True)

    def _path(self, key: str) -> Path:
        digest = hashlib.sha256(key.encode("utf-8")).hexdigest()[:24]
        return self._root / f"{digest}.png"

    def get(self, key: str) -> Path | None:
        p = self._path(key)
        return p if p.exists() else None

    def put(self, key: str, src: Path) -> Path:
        dst = self._path(key)
        if not dst.exists():
            dst.write_bytes(src.read_bytes())
        return dst