"""Release operations evidence integrity — EI-001.3 (G7/G8/G10/G12)."""

from __future__ import annotations

from pathlib import Path

import pytest

from tests.operational.helpers import render_env_map

REPO_ROOT = Path(__file__).resolve().parents[2]

FLAG_MATRIX = REPO_ROOT / "docs" / "production" / "VERSION_1_FLAG_MATRIX.md"
G7_HOLD = REPO_ROOT / "docs" / "production" / "G7_PERFORMANCE_HOLD.md"
G8_EVIDENCE = REPO_ROOT / "docs" / "production" / "G8_RELIABILITY_EVIDENCE.md"
G10_OPS = REPO_ROOT / "docs" / "production" / "G10_OPERATIONAL_EVIDENCE.md"
ENV_EXAMPLE = REPO_ROOT / ".env.example"

# Production-ON keys that must appear in both render.yaml and the G12 matrix.
PRODUCTION_ON_FLAGS = (
    "KWALITEC_V2_SOLE_RUNTIME",
    "KWALITEC_V2_STUDENT_EXPERIENCE",
    "KWALITEC_V2_DURABLE_STORE",
    "KWALITEC_V2_INJECT_ENGINES",
    "KWALITEC_V2_SEED_DEMO",
    "KWALITEC_V2_FOUNDER_INTELLIGENCE",
    "KWALITEC_EI_INTERNAL_ALPHA",
)

# High-risk OFF flags that must be listed in the matrix (claim discipline).
PRODUCTION_OFF_FLAGS = (
    "KWALITEC_DIGITAL_TWIN",
    "KWALITEC_STUDY_INSIGHTS_CUTOVER",
    "KWALITEC_UNIFIED_JOURNEY",
    "KWALITEC_PERSONAL_LEARNING_PROFILE",
    "KWALITEC_ADAPTIVE_ASSESSMENT",
)


@pytest.mark.parametrize(
    "path",
    [FLAG_MATRIX, G7_HOLD, G8_EVIDENCE, G10_OPS],
    ids=["flag_matrix", "g7_hold", "g8_evidence", "g10_ops"],
)
def test_release_operations_artefacts_exist(path: Path) -> None:
    assert path.is_file(), f"missing release operations artefact: {path}"


def test_g12_flag_matrix_lists_production_on_flags() -> None:
    text = FLAG_MATRIX.read_text(encoding="utf-8")
    for flag in PRODUCTION_ON_FLAGS:
        assert flag in text, f"G12 matrix missing production-ON flag: {flag}"
    for flag in PRODUCTION_OFF_FLAGS:
        assert flag in text, f"G12 matrix missing production-OFF flag: {flag}"
    assert "kill-switch" in text.lower() or "Kill-switch" in text
    assert "Rollback" in text or "rollback" in text


def test_g12_matrix_aligned_with_render_yaml() -> None:
    render_keys = set(render_env_map())
    for flag in PRODUCTION_ON_FLAGS:
        assert flag in render_keys, f"render.yaml missing production flag: {flag}"
    matrix = FLAG_MATRIX.read_text(encoding="utf-8")
    for flag in PRODUCTION_ON_FLAGS:
        assert flag in matrix


def test_env_example_documents_production_flag_names() -> None:
    text = ENV_EXAMPLE.read_text(encoding="utf-8")
    for flag in PRODUCTION_ON_FLAGS:
        assert flag in text, f".env.example missing flag documentation: {flag}"


def test_g7_hold_documents_claim_restriction() -> None:
    text = G7_HOLD.read_text(encoding="utf-8")
    assert "HOLD" in text
    assert "high-traffic" in text.lower()
    assert "G7.2" in text
    assert "PERFORMANCE_BASELINE" in text or "performance_benchmarks" in text


def test_g8_evidence_covers_rollback_and_backup() -> None:
    text = G8_EVIDENCE.read_text(encoding="utf-8")
    assert "G8.4" in text
    assert "G8.5" in text
    assert "BACKUP_AND_RECOVERY" in text
    assert "Rollback" in text or "rollback" in text
    assert "tabletop" in text.lower()


def test_g10_ops_does_not_claim_privacy_closed() -> None:
    text = G10_OPS.read_text(encoding="utf-8")
    assert "G10.5" in text
    assert "privacy" in text.lower()
    assert "OPEN" in text or "Open" in text
    assert "dependency_audit" in text or "DEPENDENCY_ASSURANCE" in text
