"""Domain tests for AP-002D6 Tutor explainability objects."""

from __future__ import annotations

from datetime import UTC, datetime

import pytest

from app.domain.intelligent_tutor.explainability.context import ExplanationContext
from app.domain.intelligent_tutor.explainability.errors import (
    BrokenConceptReference,
    BrokenLearningObjectiveReference,
    UnknownExplanationSchema,
)
from app.domain.intelligent_tutor.explainability.events import (
    ExplanationEventKind,
    TutorExplanationGenerated,
    TutorExplanationRequested,
    TutorExplanationUnavailable,
)
from app.domain.intelligent_tutor.explainability.explanation import TutorExplanation
from app.domain.intelligent_tutor.explainability.reference import ExplanationReference
from app.domain.intelligent_tutor.explainability.section import (
    ConceptExplanation,
    ExplanationSectionKind,
    LearningObjectiveExplanation,
    parse_section_kind,
)
from app.domain.intelligent_tutor.explainability.version import (
    EXPLANATION_VERSION,
    ExplanationVersion,
)

FIXED = datetime(2026, 7, 28, 15, 0, 0, tzinfo=UTC).replace(tzinfo=None)


def _context(**overrides) -> ExplanationContext:
    data = {
        "twin_id": "twin-1",
        "student_id": "student-1",
        "reasoning_request_id": "rr-1",
        "evidence_bundle_id": "bundle-1",
        "session_id": "sess-1",
        "correlation_id": "corr-1",
        "explanation_version": EXPLANATION_VERSION,
        "decision_version": "AP-002D3.decision.v1",
        "twin_version": 1,
        "decision_set_id": "eds-1",
    }
    data.update(overrides)
    return ExplanationContext(**data)


def _reference(**overrides) -> ExplanationReference:
    data = {
        "decision_id": "ed-1",
        "decision_version": "AP-002D3.decision.v1",
        "twin_version": 1,
        "evidence_bundle_id": "bundle-1",
        "educational_observation_ids": ("obs-1",),
        "reasoning_request_id": "rr-1",
        "assessment_session_id": "sess-1",
        "correlation_id": "corr-1",
        "explanation_version": EXPLANATION_VERSION,
        "twin_id": "twin-1",
        "concept": "concept-bayes",
        "learning_objective": "lo-bayes",
    }
    data.update(overrides)
    return ExplanationReference(**data)


def test_explanation_version_identity() -> None:
    assert EXPLANATION_VERSION == "AP-002D6.explanation.v1"
    assert str(ExplanationVersion()) == EXPLANATION_VERSION


def test_parse_section_kind_rejects_unknown() -> None:
    with pytest.raises(UnknownExplanationSchema):
        parse_section_kind("invented_kind")


def test_explanation_reference_requires_observation_ids() -> None:
    with pytest.raises(ValueError, match="educational_observation_ids"):
        _reference(educational_observation_ids=())


def test_explanation_context_derives_request_id() -> None:
    ctx = _context()
    assert ctx.explanation_request_id.startswith("xreq:rr-1:bundle-1:v1")


def test_concept_explanation_requires_concept() -> None:
    with pytest.raises(BrokenConceptReference):
        ConceptExplanation(
            section_id="sec-1",
            kind=ExplanationSectionKind.CONCEPT,
            title="Concepts",
            body="body text",
            reference=_reference(concept=""),
            primary_concept_id="",
            concept_ids=(),
            provenance={
                "decision_id": "ed-1",
                "decision_version": "AP-002D3.decision.v1",
                "twin_version": 1,
                "evidence_bundle_id": "bundle-1",
                "educational_observation_ids": ["obs-1"],
                "reasoning_request_id": "rr-1",
                "assessment_session_id": "sess-1",
                "correlation_id": "corr-1",
                "explanation_version": EXPLANATION_VERSION,
            },
        )


def test_lo_explanation_requires_learning_objective() -> None:
    with pytest.raises(BrokenLearningObjectiveReference):
        LearningObjectiveExplanation(
            section_id="sec-lo",
            kind=ExplanationSectionKind.LEARNING_OBJECTIVE,
            title="LO",
            body="body text",
            reference=_reference(learning_objective=""),
            primary_learning_objective_id="",
            learning_objective_ids=(),
            provenance={
                "decision_id": "ed-1",
                "decision_version": "AP-002D3.decision.v1",
                "twin_version": 1,
                "evidence_bundle_id": "bundle-1",
                "educational_observation_ids": ["obs-1"],
                "reasoning_request_id": "rr-1",
                "assessment_session_id": "sess-1",
                "correlation_id": "corr-1",
                "explanation_version": EXPLANATION_VERSION,
            },
        )


def test_tutor_explanation_immutable_and_traceable() -> None:
    ctx = _context()
    explanation = TutorExplanation(
        explanation_id="tex-1",
        twin_id="twin-1",
        student_id="student-1",
        context=ctx,
        sections=(),
        explanation_version=EXPLANATION_VERSION,
        twin_version=1,
        created_at=FIXED,
        summary="Unavailable honestly.",
        available=False,
    )
    assert explanation.available is False
    assert len(explanation) == 0
    with pytest.raises(Exception):
        explanation.summary = "mutated"  # type: ignore[misc]


def test_factual_events() -> None:
    requested = TutorExplanationRequested(
        event_id="e1",
        twin_id="twin-1",
        decision_set_id="eds-1",
        explanation_request_id="xreq-1",
        occurred_at=FIXED,
        explanation_version=EXPLANATION_VERSION,
    )
    generated = TutorExplanationGenerated(
        event_id="e2",
        explanation_id="tex-1",
        twin_id="twin-1",
        decision_set_id="eds-1",
        section_count=3,
        occurred_at=FIXED,
        explanation_version=EXPLANATION_VERSION,
    )
    unavailable = TutorExplanationUnavailable(
        event_id="e3",
        twin_id="twin-1",
        decision_set_id="eds-1",
        reason_code="insufficient_provenance",
        occurred_at=FIXED,
        explanation_version=EXPLANATION_VERSION,
    )
    assert requested.kind is ExplanationEventKind.REQUESTED
    assert generated.kind is ExplanationEventKind.GENERATED
    assert unavailable.kind is ExplanationEventKind.UNAVAILABLE
