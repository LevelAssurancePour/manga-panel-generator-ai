"""Qt main window — thin shell that wires handlers to widgets."""
from __future__ import annotations

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit,
)

from manga_panel_generator.app.bootstrap import Services
from manga_panel_generator.app.config import AppConfig
from manga_panel_generator.handlers.panel_handler import PanelHandler
from manga_panel_generator.handlers.page_handler import PageHandler


class MainWindow(QMainWindow):
    def __init__(self, cfg: AppConfig, services: Services) -> None:
        super().__init__()
        self._cfg = cfg
        self._services = services
        self._panel_handler = PanelHandler(services.pipeline)
        self._page_handler = PageHandler(services.exporter and services.pipeline and
                                         __import__("manga_panel_generator.services.page_composer",
                                                    fromlist=["PageComposer"]).PageComposer(cfg))
        self.setWindowTitle(f"AI Manga Panel Generator v{cfg.version}")
        self.resize(1280, 820)
        self._build_ui()

    def _build_ui(self) -> None:
        root = QWidget()
        layout = QVBoxLayout(root)
        layout.addWidget(QLabel(f"Default model: {self._cfg.default_model}"))
        self._prompt = QLineEdit()
        self._prompt.setPlaceholderText("Describe the panel…")
        layout.addWidget(self._prompt)
        btn = QPushButton("Generate Panel")
        btn.clicked.connect(self._on_generate)
        layout.addWidget(btn)
        self.setCentralWidget(root)

    def _on_generate(self) -> None:
        from manga_panel_generator.core.panel_spec import PanelSpec, ShotType, ToneMark
        spec = PanelSpec(
            panel_id="panel_0",
            prompt=self._prompt.text() or "empty classroom, lone student",
            negative_prompt="color, 3d render, watermark, text",
            shot=ShotType.MEDIUM,
            tone=ToneMark.NONE,
        )
        path = self._panel_handler.generate(spec)
        self.statusBar().showMessage(f"Saved: {path}")