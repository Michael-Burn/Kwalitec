"""Dependency assurance policy — hard pip-audit gate (EI-001.2 / ER-RB-07)."""

from __future__ import annotations

from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
CI_WORKFLOW = REPO_ROOT / ".github" / "workflows" / "ci.yml"
POLICY = REPO_ROOT / "docs" / "security" / "DEPENDENCY_ASSURANCE_POLICY.md"
ACCEPTED_MD = REPO_ROOT / "docs" / "security" / "DEPENDENCY_ACCEPTED_FINDINGS.md"
ACCEPTED_TXT = REPO_ROOT / "docs" / "security" / "dependency_accepted_vulns.txt"
AUDIT_SCRIPT = REPO_ROOT / "scripts" / "dependency_audit.sh"


def _accepted_ids() -> list[str]:
    ids: list[str] = []
    for raw in ACCEPTED_TXT.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        ids.append(line)
    return ids


def test_dependency_assurance_policy_artefacts_present() -> None:
    for path in (POLICY, ACCEPTED_MD, ACCEPTED_TXT, AUDIT_SCRIPT):
        assert path.is_file(), f"missing dependency assurance artefact: {path}"
        assert path.stat().st_size > 0, f"{path.name} appears empty"


def test_dependency_assurance_policy_states_hard_gate() -> None:
    text = POLICY.read_text(encoding="utf-8")
    for required in (
        "Critical",
        "hard gate",
        "Security HOLD",
        "dependency_accepted_vulns.txt",
        "scripts/dependency_audit.sh",
        "G10.5",
        "ER-RB-07",
    ):
        assert required in text, f"policy missing: {required}"


def test_accepted_vulns_file_non_empty_and_synced_to_register() -> None:
    ids = _accepted_ids()
    assert ids, "accepted vulns file must list at least one documented HOLD ID"
    register = ACCEPTED_MD.read_text(encoding="utf-8")
    for vuln_id in ids:
        assert vuln_id in register, (
            f"{vuln_id} in dependency_accepted_vulns.txt but missing from "
            "DEPENDENCY_ACCEPTED_FINDINGS.md"
        )


def test_accepted_findings_register_has_hold_statement() -> None:
    text = ACCEPTED_MD.read_text(encoding="utf-8")
    assert "Security HOLD" in text
    assert "Critical" in text
    assert "never" in text.lower() or "must never" in text.lower()


def test_dependency_audit_script_uses_accepted_register() -> None:
    text = AUDIT_SCRIPT.read_text(encoding="utf-8")
    assert "dependency_accepted_vulns.txt" in text
    assert "pip-audit" in text
    assert "--ignore-vuln" in text
    assert "set -euo pipefail" in text


@pytest.mark.parametrize(
    "forbidden",
    [
        "Soft gate: warn in CI",
        "pip-audit -r requirements.txt || true",
    ],
)
def test_ci_does_not_soft_fail_dependency_audit(forbidden: str) -> None:
    text = CI_WORKFLOW.read_text(encoding="utf-8")
    assert forbidden not in text, (
        f"ci.yml still soft-fails dependency audit: {forbidden}"
    )


def test_ci_invokes_dependency_audit_script() -> None:
    text = CI_WORKFLOW.read_text(encoding="utf-8")
    assert "scripts/dependency_audit.sh" in text
    assert text.count("./scripts/dependency_audit.sh") >= 2
    assert "DEPENDENCY_ASSURANCE_POLICY.md" in text
