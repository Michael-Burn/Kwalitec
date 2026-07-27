"""Assessment pipeline pure domain functions.

Transforms validated assessment events into Twin observations and educational
feedback. Does NOT perform educational reasoning — that remains in
StudentReasoningService / Educational Reasoning Engine.
"""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any

from app.domain.assessment_pipeline.assessment_event import (
    AssessmentEvent,
    AssessmentEventType,
)
from app.domain.assessment_pipeline.assessment_result import AssessmentResult
from app.domain.assessment_pipeline.feedback_source import FeedbackSource
from app.domain.assessment_pipeline.feedback_validator import (
    FeedbackValidationResult,
    validate_assessment_event,
)
from app.domain.assessment_pipeline.learning_feedback import LearningFeedback
from app.domain.student_digital_twin.observation import Observation, ObservationKind

# Map assessment evidence → existing Twin observation kinds (SDT-001 preserved).
EVENT_TO_OBSERVATION_KIND: dict[AssessmentEventType, ObservationKind] = {
    AssessmentEventType.QUESTION_ATTEMPT: ObservationKind.QUESTION_ANSWERED,
    AssessmentEventType.QUIZ_SUBMISSION: ObservationKind.QUIZ_COMPLETED,
    AssessmentEventType.MISSION_STEP_COMPLETION: (
        ObservationKind.STUDY_SESSION_COMPLETED
    ),
    AssessmentEventType.MISSION_COMPLETION: ObservationKind.STUDY_SESSION_COMPLETED,
    AssessmentEventType.REVISION_SESSION: ObservationKind.REVISION_COMPLETED,
    AssessmentEventType.WORKED_EXAMPLE_COMPLETION: (
        ObservationKind.STUDY_SESSION_COMPLETED
    ),
    AssessmentEventType.FORMULA_RECALL: ObservationKind.FORMULA_REVIEWED,
    AssessmentEventType.REFLECTION_SUBMISSION: ObservationKind.STUDY_SESSION_COMPLETED,
    AssessmentEventType.STUDY_SESSION_COMPLETION: (
        ObservationKind.STUDY_SESSION_COMPLETED
    ),
}

EVENT_TO_FEEDBACK_SOURCE: dict[AssessmentEventType, FeedbackSource] = {
    AssessmentEventType.QUESTION_ATTEMPT: FeedbackSource.QUESTION,
    AssessmentEventType.QUIZ_SUBMISSION: FeedbackSource.QUIZ,
    AssessmentEventType.MISSION_STEP_COMPLETION: FeedbackSource.MISSION_STEP,
    AssessmentEventType.MISSION_COMPLETION: FeedbackSource.MISSION_COMPLETION,
    AssessmentEventType.REVISION_SESSION: FeedbackSource.REVISION,
    AssessmentEventType.WORKED_EXAMPLE_COMPLETION: FeedbackSource.WORKED_EXAMPLE,
    AssessmentEventType.FORMULA_RECALL: FeedbackSource.FORMULA_RECALL,
    AssessmentEventType.REFLECTION_SUBMISSION: FeedbackSource.REFLECTION,
    AssessmentEventType.STUDY_SESSION_COMPLETION: FeedbackSource.STUDY_SESSION,
}

_ACTIVITY_LABELS: dict[AssessmentEventType, str] = {
    AssessmentEventType.QUESTION_ATTEMPT: "Question attempt",
    AssessmentEventType.QUIZ_SUBMISSION: "Quiz submission",
    AssessmentEventType.MISSION_STEP_COMPLETION: "Mission step completion",
    AssessmentEventType.MISSION_COMPLETION: "Mission completion",
    AssessmentEventType.REVISION_SESSION: "Revision session",
    AssessmentEventType.WORKED_EXAMPLE_COMPLETION: "Worked example completion",
    AssessmentEventType.FORMULA_RECALL: "Formula recall",
    AssessmentEventType.REFLECTION_SUBMISSION: "Reflection submission",
    AssessmentEventType.STUDY_SESSION_COMPLETION: "Study session completion",
}


def observation_kind_for_event(event: AssessmentEvent) -> ObservationKind:
    """Map an assessment event type to an SDT-001 ObservationKind."""
    return EVENT_TO_OBSERVATION_KIND[event.event_type]


def performance_label_for_event(event: AssessmentEvent) -> str:
    """Deterministic educational performance label from event evidence."""
    if event.correct is True:
        return "correct"
    if event.correct is False:
        return "incorrect"
    if event.score is not None:
        if event.score >= 0.85:
            return "strong"
        if event.score >= 0.7:
            return "adequate"
        if event.score >= 0.4:
            return "partial"
        return "weak"
    if event.event_type in {
        AssessmentEventType.MISSION_COMPLETION,
        AssessmentEventType.MISSION_STEP_COMPLETION,
        AssessmentEventType.STUDY_SESSION_COMPLETION,
        AssessmentEventType.REVISION_SESSION,
        AssessmentEventType.WORKED_EXAMPLE_COMPLETION,
        AssessmentEventType.REFLECTION_SUBMISSION,
    }:
        return "completed"
    return "recorded"


def evidence_ids_for_event(event: AssessmentEvent) -> tuple[str, ...]:
    """Opaque evidence references generated from the event."""
    ids: list[str] = [f"assessment:{event.event_id}"]
    if event.curriculum_entity_id:
        ids.append(f"entity:{event.curriculum_entity_id}")
    for concept_id in event.concept_ids:
        ids.append(f"concept:{concept_id}")
    if event.mission_id:
        ids.append(f"mission:{event.mission_id}")
    if event.step_id:
        ids.append(f"step:{event.step_id}")
    if event.activity_id:
        ids.append(f"activity:{event.activity_id}")
    return tuple(dict.fromkeys(ids))


def confidence_for_event(event: AssessmentEvent) -> float:
    """Deterministic confidence from available performance signals."""
    if event.correct is True:
        return 0.85
    if event.correct is False:
        return 0.75
    if event.score is not None:
        return round(0.5 + 0.4 * float(event.score), 4)
    if event.event_type == AssessmentEventType.MISSION_COMPLETION:
        return 0.8
    if event.event_type == AssessmentEventType.REFLECTION_SUBMISSION:
        return 0.55
    return 0.65


def suggested_next_action_for_event(event: AssessmentEvent) -> str:
    """Educational next-action suggestion (not motivational)."""
    performance = performance_label_for_event(event)
    concept = (
        event.concept_ids[0]
        if event.concept_ids
        else (event.curriculum_entity_id or "the covered concept")
    )
    if performance in {"incorrect", "weak", "partial"}:
        return (
            f"Review prerequisites and attempt recovery practice on {concept} "
            "before advancing."
        )
    if event.event_type == AssessmentEventType.MISSION_COMPLETION:
        return (
            "Continue with the next Adaptive Mission generated from updated "
            "Student Digital Twin state."
        )
    if event.event_type == AssessmentEventType.REFLECTION_SUBMISSION:
        return (
            "Use the reflection evidence in the next reasoning cycle to refine "
            "recommended focus."
        )
    if performance in {"correct", "strong", "adequate", "completed"}:
        return (
            f"Proceed to spaced practice or the next curriculum-aligned activity "
            f"for {concept}."
        )
    return (
        "Record further practice so reasoning can update mastery with more evidence."
    )


def build_observation_from_event(
    event: AssessmentEvent,
    *,
    observation_id: str | None = None,
) -> Observation:
    """Create an immutable Twin observation from an assessment event.

    Observation remains a FACT. Educational inference happens later via
    StudentReasoningService.
    """
    metadata: dict[str, Any] = {
        "assessment_event_id": event.event_id,
        "assessment_event_type": event.event_type.value,
        "activity_id": event.activity_id,
        "concept_ids": list(event.concept_ids),
        "mission_id": event.mission_id,
        "step_id": event.step_id,
        "source": event.source or "assessment_pipeline",
        "performance": performance_label_for_event(event),
    }
    if event.correct is not None:
        metadata["correct"] = bool(event.correct)
    if event.score is not None:
        metadata["score"] = float(event.score)
    if event.duration_seconds is not None:
        metadata["duration_seconds"] = int(event.duration_seconds)
    metadata.update(dict(event.metadata))

    return Observation.create(
        observation_id=observation_id or f"obs-{uuid.uuid4().hex[:16]}",
        kind=observation_kind_for_event(event),
        twin_id=event.twin_id,
        student_id=event.student_id,
        recorded_at=event.occurred_at,
        curriculum_entity_id=event.curriculum_entity_id
        or (event.concept_ids[0] if event.concept_ids else ""),
        curriculum_entity_kind=event.curriculum_entity_kind
        or ("concept" if event.concept_ids or event.curriculum_entity_id else ""),
        evidence_reference=f"assessment:{event.event_id}",
        provenance=f"assessment_pipeline:{event.event_type.value}:{event.event_id}",
        metadata=metadata,
    )


def build_assessment_result(
    event: AssessmentEvent,
    observation: Observation,
    *,
    result_id: str | None = None,
    created_at: datetime | None = None,
) -> AssessmentResult:
    """Build structured assessment result metadata (no Twin inferences)."""
    when = created_at or event.occurred_at
    return AssessmentResult(
        result_id=result_id or f"asr-{uuid.uuid4().hex[:16]}",
        event_id=event.event_id,
        twin_id=event.twin_id,
        event_type=event.event_type,
        observation_id=observation.observation_id,
        performance_label=performance_label_for_event(event),
        evidence_generated=evidence_ids_for_event(event),
        concepts_covered=tuple(
            dict.fromkeys(
                [
                    *event.concept_ids,
                    *(
                        [event.curriculum_entity_id]
                        if event.curriculum_entity_id
                        else []
                    ),
                ]
            )
        ),
        confidence=confidence_for_event(event),
        created_at=when,
        metadata={
            "mission_id": event.mission_id,
            "step_id": event.step_id,
            "activity_id": event.activity_id,
        },
    )


def build_learning_feedback(
    event: AssessmentEvent,
    result: AssessmentResult,
    *,
    feedback_id: str | None = None,
    timestamp: datetime | None = None,
) -> LearningFeedback:
    """Deterministic educational learning feedback from event + result."""
    when = timestamp or result.created_at
    return LearningFeedback(
        feedback_id=feedback_id or f"lfb-{uuid.uuid4().hex[:16]}",
        twin_id=event.twin_id,
        event_id=event.event_id,
        result_id=result.result_id,
        activity=_ACTIVITY_LABELS[event.event_type],
        performance=result.performance_label,
        evidence_generated=result.evidence_generated,
        concepts_covered=result.concepts_covered,
        confidence=result.confidence,
        suggested_next_action=suggested_next_action_for_event(event),
        timestamp=when,
        source=EVENT_TO_FEEDBACK_SOURCE.get(
            event.event_type, FeedbackSource.ASSESSMENT_PIPELINE
        ),
        observation_id=result.observation_id,
        mission_id=event.mission_id,
        metadata={
            "event_type": event.event_type.value,
            "step_id": event.step_id,
        },
    )


def prepare_pipeline_artifacts(
    event: AssessmentEvent,
    *,
    observation_id: str | None = None,
    result_id: str | None = None,
    feedback_id: str | None = None,
) -> tuple[
    FeedbackValidationResult,
    Observation | None,
    AssessmentResult | None,
    LearningFeedback | None,
]:
    """Validate event and build observation / result / feedback (pure).

    Does not touch Twin state or persistence.
    """
    validation = validate_assessment_event(event)
    if not validation.passed:
        return validation, None, None, None
    observation = build_observation_from_event(event, observation_id=observation_id)
    result = build_assessment_result(event, observation, result_id=result_id)
    feedback = build_learning_feedback(event, result, feedback_id=feedback_id)
    return validation, observation, result, feedback
