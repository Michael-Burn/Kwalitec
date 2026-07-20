"""Architecture governance documents are release artefacts (APP-003)."""

from __future__ import annotations

import pytest

from tests.architecture import ADR_ROOT, DOCS_ROOT

REQUIRED_DOCS = (
    DOCS_ROOT / "ARCHITECTURE_CONSTITUTION.md",
    DOCS_ROOT / "ARCHITECTURE_OVERVIEW.md",
    DOCS_ROOT / "SYSTEM_CONTEXT.md",
    DOCS_ROOT / "DEPENDENCY_RULES.md",
)

REQUIRED_ADRS = (
    ADR_ROOT / "README.md",
    ADR_ROOT / "ADR-001-educational-operating-system.md",
    ADR_ROOT / "ADR-002-mission-generation.md",
    ADR_ROOT / "ADR-003-study-planning.md",
    ADR_ROOT / "ADR-004-progress-evaluation.md",
    ADR_ROOT / "ADR-005-recommendation-engine.md",
    ADR_ROOT / "ADR-006-explainability-engine.md",
    ADR_ROOT / "ADR-007-student-experience.md",
    ADR_ROOT / "ADR-008-ai-enrichment-boundary.md",
    ADR_ROOT / "ADR-009-composition-root.md",
    ADR_ROOT / "ADR-010-educational-pipeline.md",
)


@pytest.mark.parametrize("path", REQUIRED_DOCS, ids=lambda p: p.name)
def test_architecture_governance_documents_exist(path) -> None:
    assert path.is_file(), f"missing release artefact {path}"
    assert path.stat().st_size > 100, f"{path.name} appears empty"


@pytest.mark.parametrize("path", REQUIRED_ADRS, ids=lambda p: p.name)
def test_architecture_adrs_exist(path) -> None:
    assert path.is_file(), f"missing ADR release artefact {path}"
    text = path.read_text(encoding="utf-8")
    assert len(text) > 100, f"{path.name} appears empty"
    if path.name.startswith("ADR-"):
        assert "Status:" in text
        assert "APP-003" in text


def test_constitution_covers_required_principles() -> None:
    text = (DOCS_ROOT / "ARCHITECTURE_CONSTITUTION.md").read_text(encoding="utf-8")
    for principle in (
        "Educational Truth",
        "Deterministic Decisions",
        "Evidence-first",
        "Explainability",
        "Student Experience Separation",
        "AI Enrichment Boundary",
        "Dependency Inversion",
        "Framework Independence",
        "Replaceable Infrastructure",
        "Testing Philosophy",
    ):
        assert principle in text, f"Constitution missing principle: {principle}"
