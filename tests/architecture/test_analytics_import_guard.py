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


def test_phase_a_has_no_domain_emit_hooks() -> None:
    """Phase A must not wire Session/reflection/journey/ESS/Twin emits.

    Match quoted event-type literals only so attribute access like
    ``session.started_at`` does not false-positive.
    """
    root = Path(__file__).resolve().parents[2] / "app"
    forbidden_emit_markers = (
        "session.started",
        "session.completed",
        "reflection.completed",
        "journey.milestone_reached",
        "educational_state.snapshot",
        "twin.evolved",
    )
    # Only scan application / services / presentation — not docs or tests.
    scan_roots = (
        root / "application",
        root / "services",
        root / "presentation",
        root / "domain",
        root / "mission",
        root / "dashboard",
    )
    for scan_root in scan_roots:
        if not scan_root.exists():
            continue
        for path in scan_root.rglob("*.py"):
            text = path.read_text(encoding="utf-8")
            for marker in forbidden_emit_markers:
                quoted = (f'"{marker}"', f"'{marker}'")
                assert not any(q in text for q in quoted), (
                    f"Phase A domain emit leak: {marker} in {path}"
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
