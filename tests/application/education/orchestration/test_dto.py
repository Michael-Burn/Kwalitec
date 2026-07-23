"""DTO construction and immutability tests."""

from __future__ import annotations

from datetime import UTC, datetime

import pytest

from application.education.orchestration.dto.educational_decision import (
    EducationalDecision,
)
from application.education.orchestration.dto.educational_evaluation import (
    EducationalEvaluation,
)
from application.education.orchestration.dto.evaluation_snapshot import (
    EvaluationSnapshot,
)
from application.education.orchestration.dto.evaluation_summary import (
    EvaluationSummary,
)
from application.education.orchestration.dto.interaction_requests import (
    InteractionKind,
    QuestionAnswerRequest,
    StudentInteractionRequest,
)

AS_OF = datetime(2026, 7, 23, 12, 0, 0, tzinfo=UTC)


def _decision() -> EducationalDecision:
    return EducationalDecision(
        decision_id="dec-1",
        category="FocusCompetency",
        subject_id="algebra",
        competency_id="linear-equations",
        priority_band="high",
        impact_band="high",
        confidence_magnitude=0.7,
        reason_summary="weak_mastery",
        rank=1,
    )


def _summary() -> EvaluationSummary:
    return EvaluationSummary(
        student_id="student-1",
        assessment_id="assessment-1",
        recommendation_set_id="set-1",
        mastery_magnitude=0.4,
        mastery_band="developing",
        confidence_magnitude=0.5,
        stability_band="moderate",
        knowledge_gap_count=1,
        recommendation_count=1,
        evidence_count=2,
        evaluated_at=AS_OF,
        top_decision_category="FocusCompetency",
    )


def test_educational_decision_immutable() -> None:
    decision = _decision()
    with pytest.raises(Exception):
        decision.rank = 2  # type: ignore[misc]


def test_evaluation_summary_requires_student_id() -> None:
    with pytest.raises(ValueError, match="student_id"):
        EvaluationSummary(
            student_id="",
            assessment_id="a",
            recommendation_set_id="s",
            mastery_magnitude=0.1,
            mastery_band="developing",
            confidence_magnitude=0.1,
            stability_band="volatile",
            knowledge_gap_count=0,
            recommendation_count=0,
            evidence_count=0,
            evaluated_at=AS_OF,
        )


def test_evaluation_snapshot_top_decision() -> None:
    decision = _decision()
    summary = _summary()
    snapshot = EvaluationSnapshot(
        student_id="student-1",
        evaluated_at=AS_OF,
        stages_completed=("compose_result",),
        summary=summary,
        decisions=(decision,),
        evidence_id="evidence-1",
    )
    assert snapshot.decision_count() == 1
    assert snapshot.top_decision() is decision


def test_successful_evaluation_factory() -> None:
    decision = _decision()
    summary = _summary()
    snapshot = EvaluationSnapshot(
        student_id="student-1",
        evaluated_at=AS_OF,
        stages_completed=("compose_result",),
        summary=summary,
        decisions=(decision,),
    )
    result = EducationalEvaluation.succeeded(
        student_id="student-1",
        stages_completed=("compose_result",),
        summary=summary,
        snapshot=snapshot,
        decisions=(decision,),
    )
    assert result.success is True
    assert result.failed_result is False


def test_failed_evaluation_factory() -> None:
    result = EducationalEvaluation.failed(
        student_id="student-1",
        stages_completed=("load_student_state",),
        failure_code="student_state_unavailable",
        failure_message="missing",
    )
    assert result.success is False
    assert result.failure_code == "student_state_unavailable"


def test_successful_evaluation_rejects_failure_fields() -> None:
    decision = _decision()
    summary = _summary()
    snapshot = EvaluationSnapshot(
        student_id="student-1",
        evaluated_at=AS_OF,
        stages_completed=("compose_result",),
        summary=summary,
        decisions=(decision,),
    )
    with pytest.raises(ValueError, match="failure"):
        EducationalEvaluation(
            success=True,
            student_id="student-1",
            stages_completed=("compose_result",),
            summary=summary,
            snapshot=snapshot,
            decisions=(decision,),
            failure_code="x",
        )


def test_student_interaction_request_requires_matching_payload() -> None:
    with pytest.raises(ValueError, match="matching payload"):
        StudentInteractionRequest(kind=InteractionKind.QUESTION_ANSWER)


def test_student_interaction_request_rejects_extra_payload() -> None:
    qa = QuestionAnswerRequest(
        student_id="s",
        competency_id="c",
        is_correct=True,
        occurred_at=AS_OF,
        learning_environment="free_practice",
    )
    from application.education.orchestration.dto.interaction_requests import (
        ReflectionRequest,
    )

    with pytest.raises(ValueError, match="exactly one"):
        StudentInteractionRequest(
            kind=InteractionKind.QUESTION_ANSWER,
            question_answer=qa,
            reflection=ReflectionRequest(
                student_id="s",
                reflection_text="notes",
                occurred_at=AS_OF,
                learning_environment="reflection_prompt",
            ),
        )
