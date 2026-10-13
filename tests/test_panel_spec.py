"""Unit tests for PanelSpec and cache key stability."""
from manga_panel_generator.core.panel_spec import PanelSpec, ShotType, ToneMark


def _make(**kw) -> PanelSpec:
    base = dict(
        panel_id="p1",
        prompt="rain on rooftop, two figures",
        negative_prompt="color",
        shot=ShotType.WIDE,
        tone=ToneMark.NONE,
    )
    base.update(kw)
    return PanelSpec(**base)


def test_cache_key_is_deterministic():
    a = _make()
    b = _make()
    assert a.cache_key() == b.cache_key()


def test_cache_key_changes_with_seed():
    assert _make(seed=1).cache_key() != _make(seed=2).cache_key()


def test_cache_key_changes_with_shot():
    assert _make(shot=ShotType.WIDE).cache_key() != _make(shot=ShotType.CLOSE_UP).cache_key()


def test_defaults_are_sane():
    s = _make()
    assert s.width == 1024 and s.height == 1024
    assert 0 < s.cfg_scale < 20
    assert s.steps > 0