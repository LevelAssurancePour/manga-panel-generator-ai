"""Entry point for the AI Manga Panel Generator desktop application."""
from __future__ import annotations

import sys
import logging
from pathlib import Path

from PySide6.QtWidgets import QApplication

from manga_panel_generator.app.config import AppConfig
from manga_panel_generator.app.bootstrap import Bootstrap
from manga_panel_generator.ui.main_window import MainWindow

logger = logging.getLogger("mpg.main")


def _configure_logging(cfg: AppConfig) -> None:
    log_dir = Path(cfg.paths.log_dir)
    log_dir.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        level=cfg.log_level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[
            logging.FileHandler(log_dir / "mpg.log", encoding="utf-8"),
            logging.StreamHandler(sys.stdout),
        ],
    )


def main() -> int:
    cfg = AppConfig.load()
    _configure_logging(cfg)
    logger.info("Booting manga-panel-generator-ai v%s", cfg.version)

    boot = Bootstrap(cfg)
    boot.warm_up()
    if boot.fatal_error:
        logger.critical("Bootstrap failed: %s", boot.fatal_error)
        return 2

    app = QApplication(sys.argv)
    window = MainWindow(cfg=cfg, services=boot.services)
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())