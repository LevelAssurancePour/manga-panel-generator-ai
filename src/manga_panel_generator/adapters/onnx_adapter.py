"""Optional ONNX Runtime adapter for CPU-only deployments."""
from __future__ import annotations

from pathlib import Path


class OnnxAdapter:
    def __init__(self, model_path: Path, providers: list[str] | None = None) -> None:
        self._model_path = model_path
        self._providers = providers or ["CPUExecutionProvider"]
        self._session = None

    def load(self) -> None:
        import onnxruntime as ort  # type: ignore
        self._session = ort.InferenceSession(
            str(self._model_path),
            providers=self._providers,
        )

    def run(self, inputs: dict) -> list:
        if self._session is None:
            self.load()
        return self._session.run(None, inputs)  # type: ignore[union-attr]