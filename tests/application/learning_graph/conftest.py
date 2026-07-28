"""Shared fixtures for AP-002D4 Learning Graph projection tests."""

from __future__ import annotations

from dataclasses import replace
from datetime import UTC, datetime
from typing import Any

from app.application.reasoning.decisions.versions import DECISION_VERSION
from app.domain.learning_graph.learning_graph import LearningGraph
from app.domain.reasoning.decisions.category import DecisionCategory
from app.domain.reasoning.decisions.context import DecisionContext
from app.domain.reasoning.decisions.decision import EducationalDecision
from app.domain.reasoning.decisions.decision_set import EducationalDecisionSet
from app.domain.reasoning.decisions.reason import DecisionReason
from app.domain.reasoning.decisions.reference import DecisionReference
from app.domain.student_digital_twin.student import Student
from app.domain.student_digital_twin.student_digital_twin import StudentDigitalTwin

FIXED_AT = datetime(2026, 7, 28, 12, 0, 0, tzinfo=UTC).replace(tzinfo=None)


def make_twin(
    *,
    twin_id: str = "twin-proj-1",
    student_id: str = "student-1",
    version: int = 1,
) -> StudentDigitalTwin:
    twin = StudentDigitalTwin.create(
        twin_id=twin_id,
        student=Student(student_id=student_id, display_name="Learner"),
        created_at=FIXED_AT,
    )
    if version != twin.version:
        twin = replace(twin, version=version)
    return twin


def make_graph(
    *,
    twin: StudentDigitalTwin | None = None,
    graph_id: str = "lg-proj-test-1",
) -> LearningGraph:
    twin = twin or make_twin()
    return LearningGraph.create(
        graph_id=graph_id,
        twin_id=twin.twin_id,
        student_id=twin.student.student_id,
        created_at=FIXED_AT,
    )


def make_decision_context(
    *,
    twin_id: str = "twin-proj-1",
    reasoning_request_id: str = "rr-1",
    evidence_bundle_id: str = "bundle-1",
    session_id: str = "sess-1",
    correlation_id: str = "corr-1",
    observation_set_id: str = "obs-set-1",
    prior_twin_version: int = 1,
    decision_version: str = DECISION_VERSION,
) -> DecisionContext:
    return DecisionContext(
        twin_id=twin_id,
        reasoning_request_id=reasoning_request_id,
        evidence_bundle_id=evidence_bundle_id,
        session_id=session_id,
        correlation_id=correlation_id,
        decision_version=decision_version,
        prior_twin_version=prior_twin_version,
        observation_set_id=observation_set_id,
    )


def make_decision(
    *,
    decision_id: str = "ed:rr-1:bundle-1:mastery_belief_update:concept-bayes",
    category: DecisionCategory = DecisionCategory.MASTERY_BELIEF_UPDATE,
    twin_id: str = "twin-proj-1",
    subject_ref: str = "concept-bayes",
    value: Any = 0.55,
    concept_reference: str = "concept-bayes",
    learning_objective_reference: str = "lo-1",
    observation_ids: tuple[str, ...] = ("obs-1",),
    evidence_bundle_id: str = "bundle-1",
    reasoning_request_id: str = "rr-1",
    session_id: str = "sess-1",
    correlation_id: str = "corr-1",
    decision_version: str = DECISION_VERSION,
    payload: dict[str, Any] | None = None,
    created_at: datetime = FIXED_AT,
) -> EducationalDecision:
    reference = DecisionReference(
        evidence_bundle_id=evidence_bundle_id,
        educational_observation_ids=observation_ids,
        reasoning_request_id=reasoning_request_id,
        assessment_session_id=session_id,
        correlation_id=correlation_id,
        learning_objective_reference=learning_objective_reference,
        concept_reference=concept_reference,
        decision_id=decision_id,
    )
    provenance = {
        "evidence_bundle_id": evidence_bundle_id,
        "educational_observation_ids": list(observation_ids),
        "reasoning_request_id": reasoning_request_id,
        "decision_id": decision_id,
        "decision_version": decision_version,
        "assessment_session_id": session_id,
        "correlation_id": correlation_id,
    }
    traceability = {
        **provenance,
        "twin_id": twin_id,
        "subject_ref": subject_ref,
    }
    return EducationalDecision(
        decision_id=decision_id,
        category=category,
        twin_id=twin_id,
        subject_ref=subject_ref,
        value=value,
        reason=DecisionReason(
            code="mastery_belief",
            summary="Mastery belief update from assessment evidence",
            detail="approved mastery rule",
            observation_ids=observation_ids,
            rule_code="MasteryUpdateRule",
        ),
        reference=reference,
        decision_version=decision_version,
        created_at=created_at,
        provenance=provenance,
        traceability=traceability,
        payload=payload
        or {
            "mastery_id": f"mst-{concept_reference}",
            "mastery_score": float(value) if isinstance(value, int | float) else 0.5,
            "confidence": 0.4,
            "trend": "improving",
            "evidence_count": 1,
        },
    )


def make_decision_set(
    *,
    twin_id: str = "twin-proj-1",
    decisions: tuple[EducationalDecision, ...] | None = None,
    set_id: str = "eds-1",
    context: DecisionContext | None = None,
) -> EducationalDecisionSet:
    context = context or make_decision_context(twin_id=twin_id)
    resolved = decisions or (
        make_decision(
            twin_id=twin_id,
            evidence_bundle_id=context.evidence_bundle_id,
            reasoning_request_id=context.reasoning_request_id,
            session_id=context.session_id,
            correlation_id=context.correlation_id,
            decision_version=context.decision_version,
        ),
    )
    return EducationalDecisionSet(
        set_id=set_id,
        decisions=resolved,
        context=context,
        decision_version=context.decision_version,
    )
