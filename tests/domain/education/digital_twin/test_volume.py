"""High-volume matrices exercising Educational Digital Twin domain surface."""

from __future__ import annotations

import pytest

from domain.education.digital_twin import (
    ConfidenceProfile,
    LearnerActivityStatus,
    MasteryBand,
    MasteryState,
    MisconceptionPresence,
    RetentionBand,
    RetentionState,
    StateTransitionIsValidSpecification,
    TwinIsConsistentSpecification,
    TwinStatus,
)
from domain.education.foundation.enums import (
    ConfidenceLevel,
    EvidenceType,
    TeachingIntentionType,
    TeachingStrategyType,
)
from domain.education.foundation.errors import EducationalInvariantViolation
from tests.domain.education.digital_twin.conftest import make_twin

STRATEGY_TYPES = list(TeachingStrategyType)
INTENTION_TYPES = list(TeachingIntentionType)
EVIDENCE_TYPES = list(EvidenceType)
MASTERY_BANDS = list(MasteryBand)
RETENTION_BANDS = list(RetentionBand)
CONFIDENCE_LEVELS = list(ConfidenceLevel)
PRESENCES = list(MisconceptionPresence)
ACTIVITIES = list(LearnerActivityStatus)
STUDENTS = tuple(f"student-{i}" for i in range(1, 11))


@pytest.mark.parametrize("strategy_type", STRATEGY_TYPES)
@pytest.mark.parametrize("student", STUDENTS)
def test_create_and_record_intervention_per_strategy_student(
    strategy_type: TeachingStrategyType, student: str
) -> None:
    twin = make_twin(
        twin_id=f"twin-{strategy_type.value}-{student}",
        student_id=student,
    )
    twin.record_intervention(
        f"int-{strategy_type.value}",
        strategy_type=strategy_type,
    )
    assert twin.student_id == student
    assert twin.intervention_history[0].strategy_type is strategy_type
    assert TwinIsConsistentSpecification().is_satisfied_by(twin)


@pytest.mark.parametrize("intention_type", INTENTION_TYPES)
@pytest.mark.parametrize("student", STUDENTS)
def test_record_intervention_per_intention_student(
    intention_type: TeachingIntentionType, student: str
) -> None:
    twin = make_twin(
        twin_id=f"twin-int-{intention_type.value}-{student}",
        student_id=student,
    )
    twin.record_intervention(
        f"int-{intention_type.value}",
        intention_type=intention_type,
    )
    assert twin.intervention_history[0].intention_type is intention_type


@pytest.mark.parametrize("evidence_type", EVIDENCE_TYPES)
@pytest.mark.parametrize("student", STUDENTS)
def test_record_evidence_per_type_student(
    evidence_type: EvidenceType, student: str
) -> None:
    twin = make_twin(
        twin_id=f"twin-ev-{evidence_type.value}-{student}",
        student_id=student,
    )
    twin.record_evidence(
        f"ev-{evidence_type.value}-{student}",
        evidence_type,
        concept_id=f"c-{evidence_type.value}",
    )
    assert twin.evidence_history[0].evidence_type is evidence_type
    assert twin.has_concept(f"c-{evidence_type.value}")


@pytest.mark.parametrize("strategy_type", STRATEGY_TYPES)
@pytest.mark.parametrize("intention_type", INTENTION_TYPES)
def test_strategy_intention_intervention_matrix(
    strategy_type: TeachingStrategyType, intention_type: TeachingIntentionType
) -> None:
    twin = make_twin(
        twin_id=f"twin-si-{strategy_type.value}-{intention_type.value}",
    )
    twin.record_intervention(
        f"int-{strategy_type.value}-{intention_type.value}",
        strategy_type=strategy_type,
        intention_type=intention_type,
    )
    entry = twin.intervention_history[0]
    assert entry.strategy_type is strategy_type
    assert entry.intention_type is intention_type


@pytest.mark.parametrize("mastery", MASTERY_BANDS)
@pytest.mark.parametrize("retention", RETENTION_BANDS)
def test_mastery_retention_concept_matrix(
    mastery: MasteryBand, retention: RetentionBand
) -> None:
    twin = make_twin(twin_id=f"twin-mr-{mastery.value}-{retention.value}")
    twin.update_mastery(
        f"c-{mastery.value}-{retention.value}",
        MasteryState.of(mastery, ratio=0.5),
    )
    twin.update_retention(
        RetentionState.of(retention, ratio=0.5),
        concept_id=f"c-{mastery.value}-{retention.value}",
    )
    state = twin.concept_state_for(f"c-{mastery.value}-{retention.value}")
    assert state is not None
    assert state.mastery.band is mastery
    assert state.retention.band is retention


@pytest.mark.parametrize("mastery", MASTERY_BANDS)
@pytest.mark.parametrize("student", STUDENTS)
def test_mastery_update_per_student(
    mastery: MasteryBand, student: str
) -> None:
    twin = make_twin(
        twin_id=f"twin-m-{mastery.value}-{student}",
        student_id=student,
    )
    twin.update_mastery("concept-m", MasteryState.of(mastery))
    assert twin.concept_state_for("concept-m").mastery.band is mastery


@pytest.mark.parametrize("retention", RETENTION_BANDS)
@pytest.mark.parametrize("student", STUDENTS)
def test_retention_update_per_student(
    retention: RetentionBand, student: str
) -> None:
    twin = make_twin(
        twin_id=f"twin-r-{retention.value}-{student}",
        student_id=student,
    )
    twin.update_retention(RetentionState.of(retention))
    assert twin.retention.band is retention


@pytest.mark.parametrize("level", CONFIDENCE_LEVELS)
@pytest.mark.parametrize("student", STUDENTS)
def test_confidence_update_per_student(
    level: ConfidenceLevel, student: str
) -> None:
    twin = make_twin(
        twin_id=f"twin-cf-{level.value}-{student}",
        student_id=student,
    )
    twin.update_confidence(ConfidenceProfile.of(level, ratio=0.4))
    assert twin.confidence.overall is level


@pytest.mark.parametrize("evidence_type", EVIDENCE_TYPES)
@pytest.mark.parametrize("mastery", MASTERY_BANDS)
def test_evidence_then_mastery_matrix(
    evidence_type: EvidenceType, mastery: MasteryBand
) -> None:
    twin = make_twin(twin_id=f"twin-em-{evidence_type.value}-{mastery.value}")
    twin.record_evidence(
        f"ev-{evidence_type.value}-{mastery.value}",
        evidence_type,
        concept_id="concept-em",
    )
    twin.update_mastery("concept-em", MasteryState.of(mastery))
    assert twin.evidence_count() == 1
    assert twin.concept_state_for("concept-em").mastery.band is mastery


@pytest.mark.parametrize("evidence_type", EVIDENCE_TYPES)
@pytest.mark.parametrize("strategy_type", STRATEGY_TYPES)
def test_evidence_then_intervention_matrix(
    evidence_type: EvidenceType, strategy_type: TeachingStrategyType
) -> None:
    twin = make_twin(
        twin_id=f"twin-ei-{evidence_type.value}-{strategy_type.value}"
    )
    twin.record_evidence(
        f"ev-{evidence_type.value}-{strategy_type.value}",
        evidence_type,
    )
    twin.record_intervention(
        f"int-{evidence_type.value}-{strategy_type.value}",
        strategy_type=strategy_type,
    )
    assert twin.evidence_count() == 1
    assert twin.intervention_count() == 1


@pytest.mark.parametrize("presence", PRESENCES)
@pytest.mark.parametrize("student", STUDENTS)
def test_misconception_presence_per_student(
    presence: MisconceptionPresence, student: str
) -> None:
    twin = make_twin(
        twin_id=f"twin-misc-{presence.value}-{student}",
        student_id=student,
    )
    twin.record_misconception_state(f"misc-{student}", presence)
    assert twin.misconception_state_for(f"misc-{student}").presence is presence


@pytest.mark.parametrize("activity", ACTIVITIES)
@pytest.mark.parametrize("student", STUDENTS)
def test_learner_activity_per_student(
    activity: LearnerActivityStatus, student: str
) -> None:
    twin = make_twin(
        twin_id=f"twin-act-{activity.value}-{student}",
        student_id=student,
        activity_status=LearnerActivityStatus.ENGAGED,
    )
    if activity is LearnerActivityStatus.ENGAGED:
        assert twin.learner_state.activity_status is activity
        return
    if twin.learner_state.activity_status is LearnerActivityStatus.JOURNEY_COMPLETE:
        return
    twin.update_learner_activity(activity)
    assert twin.learner_state.activity_status is activity


@pytest.mark.parametrize("strategy_type", STRATEGY_TYPES)
@pytest.mark.parametrize("mastery", MASTERY_BANDS)
def test_intervention_then_mastery_matrix(
    strategy_type: TeachingStrategyType, mastery: MasteryBand
) -> None:
    twin = make_twin(twin_id=f"twin-im-{strategy_type.value}-{mastery.value}")
    twin.record_intervention(
        f"int-{strategy_type.value}-{mastery.value}",
        strategy_type=strategy_type,
        concept_id="concept-im",
    )
    twin.update_mastery("concept-im", MasteryState.of(mastery))
    assert twin.intervention_history[0].strategy_type is strategy_type
    assert twin.concept_state_for("concept-im").mastery.band is mastery


@pytest.mark.parametrize("intention_type", INTENTION_TYPES)
@pytest.mark.parametrize("mastery", MASTERY_BANDS)
def test_intention_then_mastery_matrix(
    intention_type: TeachingIntentionType, mastery: MasteryBand
) -> None:
    twin = make_twin(twin_id=f"twin-itm-{intention_type.value}-{mastery.value}")
    twin.record_intervention(
        f"int-{intention_type.value}-{mastery.value}",
        intention_type=intention_type,
    )
    twin.update_mastery("concept-itm", MasteryState.of(mastery))
    assert twin.intervention_history[0].intention_type is intention_type


@pytest.mark.parametrize("presence", PRESENCES)
@pytest.mark.parametrize("evidence_type", EVIDENCE_TYPES)
def test_misconception_and_evidence_matrix(
    presence: MisconceptionPresence, evidence_type: EvidenceType
) -> None:
    twin = make_twin(twin_id=f"twin-me-{presence.value}-{evidence_type.value}")
    twin.record_misconception_state("misc-me", presence)
    twin.record_evidence(
        f"ev-{presence.value}-{evidence_type.value}",
        evidence_type,
    )
    assert twin.misconception_count() == 1
    assert twin.evidence_count() == 1


@pytest.mark.parametrize("retention", RETENTION_BANDS)
@pytest.mark.parametrize("evidence_type", EVIDENCE_TYPES)
def test_retention_and_evidence_matrix(
    retention: RetentionBand, evidence_type: EvidenceType
) -> None:
    twin = make_twin(twin_id=f"twin-re-{retention.value}-{evidence_type.value}")
    twin.update_retention(RetentionState.of(retention))
    twin.record_evidence(
        f"ev-{retention.value}-{evidence_type.value}",
        evidence_type,
    )
    assert twin.retention.band is retention
    assert twin.evidence_count() == 1


@pytest.mark.parametrize("strategy_type", STRATEGY_TYPES)
@pytest.mark.parametrize("retention", RETENTION_BANDS)
def test_strategy_retention_matrix(
    strategy_type: TeachingStrategyType, retention: RetentionBand
) -> None:
    twin = make_twin(twin_id=f"twin-sr-{strategy_type.value}-{retention.value}")
    twin.record_intervention(
        f"int-{strategy_type.value}-{retention.value}",
        strategy_type=strategy_type,
    )
    twin.update_retention(RetentionState.of(retention))
    assert twin.intervention_history[0].strategy_type is strategy_type
    assert twin.retention.band is retention


@pytest.mark.parametrize("i", range(48))
def test_append_only_evidence_volume(i: int) -> None:
    twin = make_twin(twin_id=f"twin-vol-ev-{i}")
    twin.record_evidence(f"ev-{i}", EVIDENCE_TYPES[i % len(EVIDENCE_TYPES)])
    assert twin.evidence_count() == 1
    with pytest.raises(EducationalInvariantViolation):
        twin.record_evidence(f"ev-{i}", EvidenceType.REFLECTION)


@pytest.mark.parametrize("i", range(40))
def test_archive_blocks_further_memory_volume(i: int) -> None:
    twin = make_twin(twin_id=f"twin-vol-arch-{i}")
    twin.record_evidence(f"ev-a-{i}", EvidenceType.PERFORMANCE)
    twin.archive()
    assert twin.status is TwinStatus.ARCHIVED
    with pytest.raises(EducationalInvariantViolation):
        twin.record_intervention(f"int-a-{i}")


@pytest.mark.parametrize("i", range(36))
def test_history_preservation_roundtrip_volume(i: int) -> None:
    twin = make_twin(twin_id=f"twin-vol-hist-{i}")
    twin.record_evidence(f"ev-h-{i}", EvidenceType.PERFORMANCE)
    twin.record_intervention(f"int-h-{i}")
    first_evidence = twin.evidence_history[0]
    first_intervention = twin.intervention_history[0]
    twin.record_evidence(f"ev-h2-{i}", EvidenceType.REFLECTION)
    twin.record_intervention(f"int-h2-{i}")
    assert twin.evidence_history[0] is first_evidence
    assert twin.intervention_history[0] is first_intervention
    assert twin.evidence_count() == 2
    assert twin.intervention_count() == 2


@pytest.mark.parametrize("from_status", list(TwinStatus))
@pytest.mark.parametrize("to_status", list(TwinStatus))
def test_status_transition_matrix(
    from_status: TwinStatus, to_status: TwinStatus
) -> None:
    spec = StateTransitionIsValidSpecification()
    result = spec.is_satisfied_by_status(from_status, to_status)
    if from_status is to_status:
        assert result
    elif from_status is TwinStatus.ACTIVE and to_status is TwinStatus.ARCHIVED:
        assert result
    else:
        assert not result


@pytest.mark.parametrize("level", CONFIDENCE_LEVELS)
@pytest.mark.parametrize("mastery", MASTERY_BANDS)
def test_confidence_mastery_matrix(
    level: ConfidenceLevel, mastery: MasteryBand
) -> None:
    twin = make_twin(twin_id=f"twin-cm-{level.value}-{mastery.value}")
    twin.update_confidence(ConfidenceProfile.of(level))
    twin.update_mastery("concept-cm", MasteryState.of(mastery))
    assert twin.confidence.overall is level
    assert twin.concept_state_for("concept-cm").mastery.band is mastery
