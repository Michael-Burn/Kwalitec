"""AP-002D7 — authority and architecture purity certification."""

from __future__ import annotations

from tests.certification.educational_intelligence.authority import (
    audit_authority_matrix,
    audit_dependency_direction,
    audit_student_reasoning_stop_boundaries,
)


def test_single_authority_rule() -> None:
    findings = audit_authority_matrix()
    assert findings == [], findings


def test_dependency_direction() -> None:
    findings = audit_dependency_direction()
    assert findings == [], findings


def test_student_reasoning_stop_boundaries() -> None:
    findings = audit_student_reasoning_stop_boundaries()
    assert findings == [], findings


def test_no_cyclic_stage_authority() -> None:
    """Reasoning does not import Mission/Tutor; Mission/Tutor do not decide."""
    direction = audit_dependency_direction()
    authority = audit_authority_matrix()
    assert direction == [] and authority == []
