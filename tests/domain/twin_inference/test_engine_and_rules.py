"""Domain tests for Twin Inference Engine (EI-006)."""

from __future__ import annotations

from datetime import datetime

import pytest

from app.domain.learning_evidence.evidence_event import EvidenceEvent
from app.domain.twin_inference.belief import TwinBelief
from app.domain.twin_inference.engine import TwinInferenceEngine
from app.domain.twin_inference.evidence_prep import filter_usable_evidence
from app.domain.twin_inference.knowledge_state import aggregate_knowledge_state
from app.domain.twin_inference.learning_state import LearningState
from app.domain.twin_inference.rules.assessment_outcomes import AssessmentOutcomeRule
from app.domain.twin_inference.rules.base import InferenceContext
from app.domain.twin_inference.rules.evidence_weighting import EvidenceWeightingRule
from app.domain.twin_inference.rules.prerequisite_awareness import (
    PrerequisiteAwarenessRule,
)
from app.domain.twin_inference.rules.recency import RecencyRule, recency_factor
from app.domain.twin_inference.rules.repeated_attempts import RepeatedAttemptsRule
from app.domain.twin_inference.rules.revision_events import RevisionEventRule
from app.domain.twin_inference.version import INFERENCE_VERSION


def _event(
    *,
    eid: str,
    etype: str,
    when: datetime,
    metadata: dict | None = None,
    corrects: str | None = None,
) -> EvidenceEvent:
    return EvidenceEvent(
        evidence_id=eid,
        instance_id="sci-1",
        node_stable_id="CS1.T1.S1.LO1",
        evidence_type=etype,
        occurred_at=when,
        source="student_runtime",
        recorded_at=when,
        metadata=metadata or {},
        corrects_evidence_id=corrects,
    )


def test_belief_requires_rationale() -> None:
    with pytest.raises(ValueError, match="rationale_summary"):
        TwinBelief(
            belief_id="tie-1",
            instance_id="sci-1",
            node_stable_id="CS1.T1",
            mastery_level=0.5,
            confidence_score=0.4,
            learning_state=LearningState.DEVELOPING.value,
            supporting_evidence_ids=("lee-1",),
            inference_timestamp=datetime(2026, 7, 28),
            rationale_summary="  ",
        )


def test_filter_excludes_corrected_evidence() -> None:
    t0 = datetime(2026, 7, 1)
    t1 = datetime(2026, 7, 2)
    events = (
        _event(
            eid="lee-a",
            etype="practice_attempt",
            when=t0,
            metadata={"correct": False},
        ),
        _event(
            eid="lee-b",
            etype="manual_founder_override",
            when=t1,
            metadata={"reason": "wrong node"},
            corrects="lee-a",
        ),
    )
    usable = filter_usable_evidence(events)
    assert [e.evidence_id for e in usable] == ["lee-b"]


def test_recency_factor_bands() -> None:
    as_of = datetime(2026, 7, 28)
    assert recency_factor(datetime(2026, 7, 25), as_of) == 1.0
    assert recency_factor(datetime(2026, 7, 1), as_of) == 0.85
    assert recency_factor(datetime(2026, 5, 1), as_of) == 0.70
    assert recency_factor(datetime(2026, 1, 1), as_of) == 0.55


def test_rules_are_independently_testable() -> None:
    as_of = datetime(2026, 7, 28, 12, 0, 0)
    evidence = (
        _event(
            eid="lee-1",
            etype="practice_attempt",
            when=datetime(2026, 7, 20),
            metadata={"correct": True},
        ),
        _event(
            eid="lee-2",
            etype="assessment_result",
            when=datetime(2026, 7, 22),
            metadata={"score": 80, "passed": True},
        ),
        _event(
            eid="lee-3",
            etype="revision_session",
            when=datetime(2026, 7, 25),
            metadata={"duration_minutes": 30},
        ),
    )
    ctx = InferenceContext(
        instance_id="sci-1",
        node_stable_id="CS1.T1.S1.LO1",
        evidence=evidence,
        as_of=as_of,
    )
    assert len(EvidenceWeightingRule().apply(ctx)) == 3
    assert len(RecencyRule().apply(ctx)) == 3
    attempts = RepeatedAttemptsRule().apply(ctx)
    assert len(attempts) == 1
    assert attempts[0].mastery_delta == 0.12
    assert len(AssessmentOutcomeRule().apply(ctx)) >= 1
    assert len(RevisionEventRule().apply(ctx)) == 1

    prereq_ctx = InferenceContext(
        instance_id="sci-1",
        node_stable_id="CS1.T1.S1.LO1",
        evidence=evidence,
        as_of=as_of,
        prerequisite_mastery={"CS1.T1.S1.LO0": 0.1},
        metadata={"provisional_mastery": 0.9},
    )
    caps = PrerequisiteAwarenessRule().apply(prereq_ctx)
    assert caps[0].mastery_delta < 0


def test_engine_deterministic_and_explainable() -> None:
    as_of = datetime(2026, 7, 28, 12, 0, 0)
    evidence = (
        _event(
            eid="lee-1",
            etype="reading_completed",
            when=datetime(2026, 7, 10),
            metadata={"duration_minutes": 20},
        ),
        _event(
            eid="lee-2",
            etype="practice_attempt",
            when=datetime(2026, 7, 15),
            metadata={"correct": True},
        ),
        _event(
            eid="lee-3",
            etype="assessment_result",
            when=datetime(2026, 7, 20),
            metadata={"score": 70, "passed": True},
        ),
    )
    engine = TwinInferenceEngine()
    a = engine.infer_node_belief(
        belief_id="tie-a",
        instance_id="sci-1",
        node_stable_id="CS1.T1.S1.LO1",
        evidence=evidence,
        as_of=as_of,
    )
    b = engine.infer_node_belief(
        belief_id="tie-a",
        instance_id="sci-1",
        node_stable_id="CS1.T1.S1.LO1",
        evidence=evidence,
        as_of=as_of,
    )
    assert a.belief.to_dict() == b.belief.to_dict()
    assert a.explanation.to_dict() == b.explanation.to_dict()
    assert a.belief.inference_version == INFERENCE_VERSION
    assert a.belief.supporting_evidence_ids == ("lee-1", "lee-2", "lee-3")
    assert a.explanation.contributing_rules
    assert a.explanation.confidence_calculation.formula
    assert a.belief.mastery_level > 0
    assert a.belief.learning_state != LearningState.UNKNOWN.value


def test_unknown_belief_when_no_evidence() -> None:
    result = TwinInferenceEngine().infer_node_belief(
        belief_id="tie-empty",
        instance_id="sci-1",
        node_stable_id="CS1.T1.S1.LO1",
        evidence=(),
        as_of=datetime(2026, 7, 28),
    )
    assert result.belief.learning_state == LearningState.UNKNOWN.value
    assert result.belief.mastery_level == 0.0
    assert "No usable learning evidence" in result.belief.rationale_summary


def test_founder_absolute_override() -> None:
    as_of = datetime(2026, 7, 28)
    evidence = (
        _event(
            eid="lee-ov",
            etype="manual_founder_override",
            when=as_of,
            metadata={
                "reason": "Prior study confirmed",
                "mastery": 0.9,
                "confidence": 0.8,
            },
        ),
    )
    result = TwinInferenceEngine().infer_node_belief(
        belief_id="tie-ov",
        instance_id="sci-1",
        node_stable_id="CS1.T1.S1.LO1",
        evidence=evidence,
        as_of=as_of,
    )
    assert result.belief.mastery_level == 0.9
    assert result.belief.confidence_score == 0.8


def test_subject_knowledge_state_aggregation() -> None:
    as_of = datetime(2026, 7, 28)
    engine = TwinInferenceEngine()
    b1 = engine.infer_node_belief(
        belief_id="tie-1",
        instance_id="sci-1",
        node_stable_id="CS1.T1.S1.LO1",
        evidence=(
            _event(
                eid="lee-1",
                etype="study_session",
                when=datetime(2026, 7, 20),
                metadata={"duration_minutes": 40},
            ),
        ),
        as_of=as_of,
    ).belief
    b2 = engine.infer_node_belief(
        belief_id="tie-2",
        instance_id="sci-1",
        node_stable_id="CS1.T1.S1.LO2",
        evidence=(),
        as_of=as_of,
    ).belief
    state = aggregate_knowledge_state(
        instance_id="sci-1",
        subject_code="CS1",
        beliefs=(b1, b2),
        inferred_at=as_of,
    )
    assert state.node_belief_count == 2
    assert state.mean_mastery == round((b1.mastery_level + b2.mastery_level) / 2, 6)
    assert dict(state.learning_state_counts)[LearningState.UNKNOWN.value] == 1
