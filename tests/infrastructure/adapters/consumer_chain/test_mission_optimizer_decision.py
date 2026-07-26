"""EP-002.2 — MissionOptimizer quarantine / deprecation tests."""

from __future__ import annotations

import warnings
from unittest.mock import MagicMock

from app.services.mission_optimizer import MissionOptimizer


def test_generate_balanced_mission_emits_deprecation_warning(monkeypatch) -> None:
    monkeypatch.setattr(
        MissionOptimizer,
        "_from_canonical_plan",
        staticmethod(lambda user_id, foundation=None, canonical_state=None: None),
    )
    monkeypatch.setattr(
        MissionOptimizer,
        "_from_legacy_services",
        staticmethod(lambda user_id: None),
    )
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        result = MissionOptimizer.generate_balanced_mission(1)
    assert result is None
    assert any(issubclass(w.category, DeprecationWarning) for w in caught)
    assert any("quarantined" in str(w.message).lower() for w in caught)


def test_canonical_path_forwards_foundation_di(monkeypatch) -> None:
    foundation = MagicMock()
    state = object()
    seen: dict[str, object] = {}

    def fake_plan(user_id, today=None, *, foundation=None, canonical_state=None):
        seen["foundation"] = foundation
        seen["canonical_state"] = canonical_state
        return None

    monkeypatch.setattr(
        "app.services.planning_service.PlanningService.build_daily_study_plan",
        staticmethod(fake_plan),
    )
    monkeypatch.setattr(
        MissionOptimizer,
        "_from_legacy_services",
        staticmethod(lambda user_id: {"topic_count": 0}),
    )

    with warnings.catch_warnings():
        warnings.simplefilter("ignore", DeprecationWarning)
        MissionOptimizer.generate_balanced_mission(
            9, foundation=foundation, canonical_state=state
        )

    assert seen["foundation"] is foundation
    assert seen["canonical_state"] is state


def test_no_app_production_callers() -> None:
    """Guard: MissionOptimizer must remain unwired in application packages."""
    import pathlib
    import re

    root = pathlib.Path(__file__).resolve().parents[3] / "app"
    pattern = re.compile(
        r"MissionOptimizer|generate_balanced_mission|mission_optimizer"
    )
    offenders: list[str] = []
    for path in root.rglob("*.py"):
        if path.name == "mission_optimizer.py":
            continue
        text = path.read_text(encoding="utf-8")
        if pattern.search(text):
            # recommendation_service mentions MissionOptimizer in a docstring
            # about extracted modules — allow doc-only mentions without imports.
            if "from app.services.mission_optimizer" in text:
                offenders.append(str(path))
            elif "MissionOptimizer." in text or "generate_balanced_mission(" in text:
                offenders.append(str(path))
    assert offenders == []
