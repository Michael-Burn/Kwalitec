"""Explanation generation tests."""

from __future__ import annotations

import pytest

from app.application.student_experience.explanation_service import ExplanationService
from app.domain.student_experience.recommendation_explanation import (
    FORBIDDEN_INTERNAL_TERMS,
    is_student_safe,
)
from tests.application.student_experience.helpers import (
    FakeAdaptivePort,
    make_experience,
)

INTERNAL_PAYLOADS = [
    {
        "topic_title": "Tax",
        "reason_codes": ("high_roi",),
        "evidence_points": ("Digital Twin shows weak recall",),
        "expected_benefit": "Raise Readiness Score",
        "priority_band": "high",
    },
    {
        "topic_title": "Ethics",
        "reason_codes": ("exam_proximity",),
        "evidence_points": ("Adaptive Decision Engine ranks this high",),
        "expected_benefit": "Mission Engine session will help",
    },
    {
        "topic_title": "Audit",
        "reason_codes": ("low_retention",),
        "evidence_points": ("Learning Orchestrator noted gap",),
        "expected_benefit": "Student Digital Twin benefit",
    },
]


@pytest.mark.parametrize("payload", INTERNAL_PAYLOADS)
def test_explanation_translates_internal_payloads(payload):
    svc = ExplanationService(adaptive_decision=FakeAdaptivePort())
    expl = svc.from_opaque(payload)
    for term in FORBIDDEN_INTERNAL_TERMS:
        assert term.lower() not in expl.summary.lower()
        assert term.lower() not in expl.why_recommended.lower()
        assert term.lower() not in expl.expected_benefit.lower()
        for p in expl.evidence_points:
            assert term.lower() not in p.lower()
    assert is_student_safe(expl.summary)


@pytest.mark.parametrize("i", range(15))
def test_facade_explain_stable(i):
    expl = make_experience().explain("stu-1")
    assert expl.is_complete
    assert is_student_safe(expl.why_recommended)
