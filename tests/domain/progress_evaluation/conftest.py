"""Shared factories for Progress Evaluation domain tests (EDU-003)."""

from __future__ import annotations

import pytest

from domain.education.digital_twin import (
    EducationalDigitalTwin,
    MasteryBand,
    MasteryState,
    MisconceptionPresence,
    RetentionBand,
    RetentionState,
)
from domain.education.evidence import EvidenceItemKind, EvidenceRecord
from domain.education.foundation.enums import ConfidenceLevel
from domain.education.foundation.ids import ConceptId
from domain.mission_generation.ids import MissionSpecificationId
from domain.progress_evaluation import (
    CompletedMission,
    ProgressEvaluator,
    ProgressReport,
)
from domain.study_planning import StudyPlan
from tests.domain.education.digital_twin.conftest import (
    CONCEPT_001,
    make_confidence,
    make_retention,
    make_twin,
)
from tests.domain.education.evidence.conftest import (
    make_item,
    make_record,
    make_strength,
    make_timestamp,
)
from tests.domain.study_planning.conftest import plan_study


@pytest.fixture
def student_id() -> str:
    return "student-ada"


def make_progress_twin(
    *,
    twin_id: str = "twin-001",
    student_id: str = "student-ada",
    mastery_band: MasteryBand = MasteryBand.DEVELOPING,
    mastery_ratio: float | None = 0.55,
    retention_band: RetentionBand = RetentionBand.STABLE,
    confidence_level: ConfidenceLevel = ConfidenceLevel.MEDIUM,
    with_misconception: bool = False,
) -> EducationalDigitalTwin:
    twin = make_twin(
        twin_id=twin_id,
        student_id=student_id,
        retention=make_retention(retention_band, ratio=0.7),
        confidence=make_confidence(confidence_level, ratio=0.6),
    )
    twin.update_mastery(
        CONCEPT_001,
        MasteryState.of(mastery_band, ratio=mastery_ratio),
    )
    twin.update_retention(
        RetentionState.of(retention_band, ratio=0.7),
        concept_id=CONCEPT_001,
    )
    if with_misconception:
        twin.record_misconception_state(
            "misc-001",
            MisconceptionPresence.ACTIVE,
            related_concept_id=CONCEPT_001,
        )
    twin.pull_events()
    return twin


def make_evidence_batch(
    *,
    student_id: str = "student-ada",
    strengths: tuple[str, ...] = ("strong", "strong", "strong", "strong"),
    kind: EvidenceItemKind = EvidenceItemKind.QUESTION_RESPONSE,
    start_day: int = 1,
) -> tuple[EvidenceRecord, ...]:
    records: list[EvidenceRecord] = []
    for index, strength in enumerate(strengths):
        day = start_day + index
        records.append(
            make_record(
                evidence_id=f"evidence-{index + 1:03d}",
                student_id=student_id,
                items=[
                    make_item(
                        item_id=f"item-{index + 1:03d}",
                        kind=kind,
                        observation=f"Observation {index + 1}",
                    )
                ],
                strength=make_strength(level=strength),
                timestamp=make_timestamp(day=day, hour=10 + index),
            )
        )
    return tuple(records)


def make_completed_mission(
    *,
    mission_id: str = "mission-001",
    student_id: str = "student-ada",
    completion_sequence: int = 1,
    success: bool = True,
    outcome_millipoints: int | None = None,
    concept_ids: tuple[ConceptId, ...] | None = None,
) -> CompletedMission:
    if outcome_millipoints is None:
        outcome_millipoints = 850 if success else 200
    return CompletedMission(
        mission_id=MissionSpecificationId(mission_id),
        student_id=student_id,
        completion_sequence=completion_sequence,
        success=success,
        outcome_millipoints=outcome_millipoints,
        concept_ids=concept_ids if concept_ids is not None else (CONCEPT_001,),
    )


def evaluate_progress(
    *,
    twin: EducationalDigitalTwin | None = None,
    evidence: tuple[EvidenceRecord, ...] | None = None,
    completed_missions: tuple[CompletedMission, ...] | None = None,
    study_plans: tuple[StudyPlan, ...] | None = None,
) -> ProgressReport:
    twin = twin or make_progress_twin()
    evidence = evidence if evidence is not None else make_evidence_batch()
    completed_missions = (
        completed_missions
        if completed_missions is not None
        else (make_completed_mission(),)
    )
    study_plans = study_plans if study_plans is not None else (plan_study(),)
    return ProgressEvaluator.evaluate(
        twin,
        evidence,
        completed_missions,
        study_plans,
    )
