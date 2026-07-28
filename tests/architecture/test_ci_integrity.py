"""CI workflow integrity — sole canonical GitHub Actions authority (EI-001.1)."""

from __future__ import annotations

from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
WORKFLOWS_DIR = REPO_ROOT / ".github" / "workflows"
CANONICAL_WORKFLOW = WORKFLOWS_DIR / "ci.yml"

# Retired secondary workflow (ER-RB-01 / ER-TD-C01). Must not return.
RETIRED_WORKFLOWS = ("tests.yml",)

REQUIRED_JOB_NAME_MARKERS = (
    "name: Architecture Governance",
    "name: Unit Tests",
    "name: Integration Tests",
    "name: Educational Intelligence Certification",
    "name: Lint",
    "name: Production Gates",
    "name: Release Build",
)

REQUIRED_JOB_KEYS = (
    "architecture:",
    "unit:",
    "integration:",
    "educational-intelligence-certification:",
    "lint:",
    "production-gates:",
    "release-build:",
)


def test_workflows_directory_contains_only_canonical_ci() -> None:
    assert WORKFLOWS_DIR.is_dir(), "missing .github/workflows"
    names = sorted(p.name for p in WORKFLOWS_DIR.glob("*.yml"))
    assert names == ["ci.yml"], f"unexpected workflow files: {names}"
    for retired in RETIRED_WORKFLOWS:
        assert not (WORKFLOWS_DIR / retired).exists(), (
            f"retired workflow must not exist: {retired}"
        )


def test_canonical_ci_workflow_is_kwalitec_ci() -> None:
    text = CANONICAL_WORKFLOW.read_text(encoding="utf-8")
    assert text.lstrip().startswith("#") or text.lstrip().startswith("name:")
    assert "name: Kwalitec CI" in text
    for job_key in REQUIRED_JOB_KEYS:
        assert job_key in text, f"ci.yml missing required job key: {job_key}"
    for marker in REQUIRED_JOB_NAME_MARKERS:
        assert marker in text, f"ci.yml missing job display name: {marker}"


def test_unit_matrix_uses_supported_python_only() -> None:
    text = CANONICAL_WORKFLOW.read_text(encoding="utf-8")
    # Unit matrix must list supported versions and must not advertise 3.14.
    assert 'python-version: ["3.11", "3.12", "3.13"]' in text
    assert '"3.14"' not in text
    assert "python-version: \"3.14\"" not in text


@pytest.mark.parametrize(
    "needle",
    [
        "tests/architecture/",
        "ruff check",
        "educational-intelligence-certification",
        "pip-audit",
    ],
)
def test_canonical_ci_embeds_hard_gate_signals(needle: str) -> None:
    text = CANONICAL_WORKFLOW.read_text(encoding="utf-8")
    assert needle in text, f"ci.yml missing gate signal: {needle}"


def test_canonical_ci_dependency_audit_is_hard_gated() -> None:
    """EI-001.2 / ER-RB-07 — soft pip-audit must not return."""
    text = CANONICAL_WORKFLOW.read_text(encoding="utf-8")
    assert "scripts/dependency_audit.sh" in text
    assert "Soft gate: warn in CI" not in text
    assert "pip-audit -r requirements.txt || true" not in text


def test_release_candidate_fingerprint_doc_present() -> None:
    path = REPO_ROOT / "docs" / "production" / "RELEASE_CANDIDATE_FINGERPRINT.md"
    text = path.read_text(encoding="utf-8")
    for required in (
        "Sole CI authority",
        "commit_sha",
        "ci_run_url",
        "Engineering evidence chain",
        ".github/workflows/ci.yml",
    ):
        assert required in text, f"fingerprint doc missing: {required}"
