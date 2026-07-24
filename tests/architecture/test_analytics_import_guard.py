"""Architecture import guard — analytics must not become a second brain."""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

ANALYTICS_ROOT = (
    Path(__file__).resolve().parents[2]
    / "app"
    / "infrastructure"
    / "analytics"
)

# Modules / prefixes that would pull educational calculation into analytics.
FORBIDDEN_EXACT = frozenset(
    {
        "numpy",
        "scipy",
        "sklearn",
        "openai",
        "anthropic",
    }
)

FORBIDDEN_PREFIXES = (
    "app.domain.twin",
    "app.application.student_twin",
    "app.application.educational_state",
    "app.services.recommendation",
    "app.services.mission",
    "app.services.adaptive",
    "app.services.mastery",
    "src.domain.education.mastery_estimation",
    "src.domain.education.recommendation_engine",
    "src.domain.education.digital_twin",
    "app.infrastructure.adapters.student_twin",
    "app.infrastructure.adapters.adaptive",
    "app.infrastructure.engines",
)

FORBIDDEN_NAME_SUBSTRINGS = (
    "calculate_mastery",
    "estimate_mastery",
    "rank_recommendation",
    "generate_mission",
    "compute_readiness",
)


def _iter_python_files(root: Path) -> list[Path]:
    return sorted(root.rglob("*.py"))


def _imported_modules(path: Path) -> list[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    names: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                names.append(alias.name)
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                names.append(node.module)
    return names


@pytest.mark.parametrize(
    "path",
    _iter_python_files(ANALYTICS_ROOT),
    ids=lambda p: str(p.relative_to(ANALYTICS_ROOT)),
)
def test_analytics_no_forbidden_imports(path: Path) -> None:
    for name in _imported_modules(path):
        top = name.split(".", 1)[0]
        assert top not in FORBIDDEN_EXACT, f"{path} imports {name}"
        for prefix in FORBIDDEN_PREFIXES:
            assert not (
                name == prefix or name.startswith(prefix + ".")
            ), f"{path} imports educational module {name}"


@pytest.mark.parametrize(
    "path",
    _iter_python_files(ANALYTICS_ROOT),
    ids=lambda p: str(p.relative_to(ANALYTICS_ROOT)),
)
def test_analytics_no_educational_math_symbols(path: Path) -> None:
    source = path.read_text(encoding="utf-8").lower()
    for needle in FORBIDDEN_NAME_SUBSTRINGS:
        assert needle not in source, f"{path} contains forbidden symbol {needle}"


def test_phase_e_allows_authorised_emits_only() -> None:
    """Phase E may emit session/reflection/ESS/journey/twin events on allowlist.

    ``session.cancelled`` and legacy ``journey.milestone_reached`` remain forbidden.
    """
    root = Path(__file__).resolve().parents[2] / "app"
    allowed_session_markers = (
        "session.started",
        "session.completed",
    )
    allowed_reflection_markers = (
        "reflection.submitted",
        "reflection.completed",
    )
    allowed_ess_markers = ("educational_state.snapshot",)
    allowed_journey_markers = ("journey.progressed",)
    allowed_twin_markers = ("twin.evolved",)
    deferred_emit_markers = (
        "journey.milestone_reached",
        "session.cancelled",
    )
    allowed_session_emit_paths = frozenset(
        {
            "services/study_session_service.py",
            "infrastructure/analytics/session_events.py",
            "infrastructure/analytics/registry.py",
            "infrastructure/analytics/__init__.py",
        }
    )
    allowed_reflection_emit_paths = frozenset(
        {
            "application/learning_session/reflection_manager.py",
            "infrastructure/analytics/reflection_events.py",
            "infrastructure/analytics/registry.py",
            "infrastructure/analytics/__init__.py",
        }
    )
    allowed_ess_emit_paths = frozenset(
        {
            "application/educational_state/__init__.py",
            "infrastructure/analytics/educational_state_events.py",
            "infrastructure/analytics/registry.py",
            "infrastructure/analytics/__init__.py",
        }
    )
    allowed_journey_emit_paths = frozenset(
        {
            "application/learning_journey/journey_observation.py",
            "infrastructure/analytics/journey_events.py",
            "infrastructure/analytics/registry.py",
            "infrastructure/analytics/__init__.py",
        }
    )
    allowed_twin_emit_paths = frozenset(
        {
            "application/twin_repository/observation.py",
            "infrastructure/analytics/twin_events.py",
            "infrastructure/analytics/registry.py",
            "infrastructure/analytics/__init__.py",
        }
    )
    scan_roots = (
        root / "application",
        root / "services",
        root / "presentation",
        root / "domain",
        root / "mission",
        root / "dashboard",
        root / "infrastructure",
    )
    for scan_root in scan_roots:
        if not scan_root.exists():
            continue
        for path in scan_root.rglob("*.py"):
            text = path.read_text(encoding="utf-8")
            rel = str(path.relative_to(root)).replace("\\", "/")
            for marker in deferred_emit_markers:
                quoted = (f'"{marker}"', f"'{marker}'")
                assert not any(q in text for q in quoted), (
                    f"Phase E deferred emit leak: {marker} in {path}"
                )
            for marker in allowed_session_markers:
                quoted = (f'"{marker}"', f"'{marker}'")
                if any(q in text for q in quoted):
                    assert rel in allowed_session_emit_paths, (
                        f"session emit outside authorised path: {marker} in {path}"
                    )
            for marker in allowed_reflection_markers:
                quoted = (f'"{marker}"', f"'{marker}'")
                if any(q in text for q in quoted):
                    assert rel in allowed_reflection_emit_paths, (
                        f"reflection emit outside authorised path: "
                        f"{marker} in {path}"
                    )
            for marker in allowed_ess_markers:
                quoted = (f'"{marker}"', f"'{marker}'")
                if any(q in text for q in quoted):
                    assert rel in allowed_ess_emit_paths, (
                        f"ESS snapshot emit outside authorised path: "
                        f"{marker} in {path}"
                    )
            for marker in allowed_journey_markers:
                quoted = (f'"{marker}"', f"'{marker}'")
                if any(q in text for q in quoted):
                    assert rel in allowed_journey_emit_paths, (
                        f"journey emit outside authorised path: "
                        f"{marker} in {path}"
                    )
            for marker in allowed_twin_markers:
                quoted = (f'"{marker}"', f"'{marker}'")
                if any(q in text for q in quoted):
                    assert rel in allowed_twin_emit_paths, (
                        f"twin emit outside authorised path: {marker} in {path}"
                    )


def test_adr_025_exists() -> None:
    adr = (
        Path(__file__).resolve().parents[2]
        / "docs"
        / "adr"
        / "ADR-025-analytics-event-infrastructure.md"
    )
    assert adr.is_file()
    text = adr.read_text(encoding="utf-8")
    assert "ANALYTICS_EVENTS_V1" in text
    assert "observe" in text.lower()


def test_adr_026_exists() -> None:
    adr = (
        Path(__file__).resolve().parents[2]
        / "docs"
        / "adr"
        / "ADR-026-phase-e-journey-twin-observation.md"
    )
    assert adr.is_file()
    text = adr.read_text(encoding="utf-8")
    assert "journey.progressed" in text
    assert "twin.evolved" in text
    assert "LearningJourneyRepository" in text
