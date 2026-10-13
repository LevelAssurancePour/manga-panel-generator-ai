"""Headless CLI — batch-generate panels from a JSON storyboard."""
from __future__ import annotations

import argparse
import json
import sys

from manga_panel_generator.app.config import AppConfig
from manga_panel_generator.app.bootstrap import Bootstrap
from manga_panel_generator.core.panel_spec import PanelSpec, ShotType, ToneMark


def _spec_from_dict(d: dict) -> PanelSpec:
    return PanelSpec(
        panel_id=d["panel_id"],
        prompt=d["prompt"],
        negative_prompt=d.get("negative_prompt", "color, 3d, watermark"),
        shot=ShotType(d.get("shot", "medium")),
        tone=ToneMark(d.get("tone", "none")),
        width=d.get("width", 1024),
        height=d.get("height", 1024),
        seed=d.get("seed", -1),
        steps=d.get("steps", 28),
        cfg_scale=d.get("cfg_scale", 6.5),
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="mpg", description="AI Manga Panel Generator CLI")
    parser.add_argument("storyboard", help="path to storyboard JSON")
    parser.add_argument("--out", default=None, help="override export dir")
    args = parser.parse_args(argv)

    cfg = AppConfig.load()
    boot = Bootstrap(cfg)
    boot.warm_up()
    if boot.fatal_error or boot.services is None:
        print(f"bootstrap failed: {boot.fatal_error}", file=sys.stderr)
        return 2

    with open(args.storyboard, encoding="utf-8") as fh:
        data = json.load(fh)

    specs = [_spec_from_dict(p) for p in data["panels"]]
    paths = boot.services.pipeline.run_batch(specs)
    for p in paths:
        print(p)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())