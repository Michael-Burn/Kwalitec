"""High-volume matrices exercising Educational Orchestrator domain surface."""

from __future__ import annotations

import pytest

from domain.education.foundation.enums import TeachingStrategyType
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.foundation.ids import LearningEpisodeId
from domain.education.orchestrator import (
    EvidenceCollectionPointKind,
    OrchestrationIsValidSpecification,
    OrchestrationStageKind,
    OrchestrationStatus,
    SequencingPolicy,
    StageIsExecutableSpecification,
    StageStatus,
)
from tests.domain.education.orchestrator.conftest import (
    CANONICAL_STAGE_KINDS,
    advance_all_required,
    make_canonical_stages,
    make_orchestrator,
    make_plan,
    make_stage,
    make_started_orchestrator,
    make_strategy_ref,
)

STRATEGY_TYPES = list(TeachingStrategyType)
STAGE_KINDS = list(OrchestrationStageKind)
EVIDENCE_POINTS = list(EvidenceCollectionPointKind)
STUDENTS = tuple(f"student-{i}" for i in range(1, 9))
ACTIONS = ("start", "advance", "pause", "resume", "complete")
STATUSES = list(OrchestrationStatus)


@pytest.mark.parametrize("strategy_type", STRATEGY_TYPES)
@pytest.mark.parametrize("student", STUDENTS)
def test_create_per_strategy_and_student(
    strategy_type: TeachingStrategyType, student: str
) -> None:
    orch = make_orchestrator(
        orchestrator_id=f"orch-{strategy_type.value}-{student}",
        student_id=student,
        strategy_type=strategy_type,
    )
    assert orch.student_id == student
    assert orch.strategy_references[0].strategy_type is strategy_type
    assert orch.is_planned()
    assert OrchestrationIsValidSpecification().is_satisfied_by(orch)


@pytest.mark.parametrize("strategy_type", STRATEGY_TYPES)
@pytest.mark.parametrize("student", STUDENTS)
def test_start_and_executable_per_strategy_student(
    strategy_type: TeachingStrategyType, student: str
) -> None:
    orch = make_orchestrator(
        orchestrator_id=f"orch-start-{strategy_type.value}-{student}",
        student_id=student,
        strategy_type=strategy_type,
    )
    orch.start()
    assert orch.is_active()
    assert StageIsExecutableSpecification().is_satisfied_by(orch)


@pytest.mark.parametrize("kind", STAGE_KINDS)
@pytest.mark.parametrize("strategy_type", STRATEGY_TYPES)
def test_stage_kind_with_strategy_plan(
    kind: OrchestrationStageKind, strategy_type: TeachingStrategyType
) -> None:
    evidence = None
    if kind is OrchestrationStageKind.EVIDENCE_COLLECTION:
        evidence = EvidenceCollectionPointKind.AFTER_EPISODE
    stages = [
        make_stage(
            stage_id=f"s-{kind.value}",
            kind=kind,
            sequence_index=0,
            evidence_collection_point=evidence,
        )
    ]
    orch = make_orchestrator(
        orchestrator_id=f"orch-{kind.value}-{strategy_type.value}",
        strategy_type=strategy_type,
        plan=make_plan(plan_id=f"p-{kind.value}", stages=stages),
    )
    assert orch.stages[0].kind is kind
    orch.start()
    assert orch.stages[0].is_active() or orch.state.current_stage_id is not None


@pytest.mark.parametrize("kind", STAGE_KINDS)
@pytest.mark.parametrize("student", STUDENTS)
def test_pause_resume_per_stage_kind_context(
    kind: OrchestrationStageKind, student: str
) -> None:
    # Use full canonical plan; kind only diversifies identity.
    orch = make_orchestrator(
        orchestrator_id=f"orch-pr-{kind.value}-{student}",
        student_id=student,
    )
    orch.start()
    orch.pause(f"pause-{kind.value}")
    assert orch.is_paused()
    orch.resume()
    assert orch.is_active()


@pytest.mark.parametrize("point", EVIDENCE_POINTS)
@pytest.mark.parametrize("strategy_type", STRATEGY_TYPES)
def test_evidence_collection_point_matrix(
    point: EvidenceCollectionPointKind, strategy_type: TeachingStrategyType
) -> None:
    stages = [
        make_stage(
            stage_id="create",
            kind=OrchestrationStageKind.EPISODE_CREATION,
            sequence_index=0,
        ),
        make_stage(
            stage_id="evidence",
            kind=OrchestrationStageKind.EVIDENCE_COLLECTION,
            sequence_index=1,
            evidence_collection_point=point,
        ),
    ]
    orch = make_orchestrator(
        orchestrator_id=f"orch-ev-{point.value}-{strategy_type.value}",
        strategy_type=strategy_type,
        plan=make_plan(stages=stages),
    )
    orch.start()
    orch.advance()
    assert orch.progress.evidence_collection_points_reached == 0
    orch.advance()
    assert orch.progress.evidence_collection_points_reached == 1
    assert orch.progress.evidence_points_complete


@pytest.mark.parametrize("strategy_type", STRATEGY_TYPES)
@pytest.mark.parametrize("student", STUDENTS[:6])
def test_complete_lifecycle_matrix(
    strategy_type: TeachingStrategyType, student: str
) -> None:
    orch = make_orchestrator(
        orchestrator_id=f"orch-life-{strategy_type.value}-{student}",
        student_id=student,
        strategy_type=strategy_type,
    )
    orch.start()
    advance_all_required(orch)
    orch.complete()
    assert orch.is_completed()
    assert orch.status is OrchestrationStatus.COMPLETED


@pytest.mark.parametrize("kind", STAGE_KINDS)
@pytest.mark.parametrize("student", STUDENTS[:6])
def test_sequencing_progress_per_kind_seed(
    kind: OrchestrationStageKind, student: str
) -> None:
    stages = make_canonical_stages()
    # Ensure kind appears (canonical already has all).
    assert any(s.kind is kind for s in stages)
    orch = make_orchestrator(
        orchestrator_id=f"orch-seq-{kind.value}-{student}",
        student_id=student,
        plan=make_plan(stages=stages),
    )
    orch.start()
    progress = SequencingPolicy.progress_of(orch.stages)
    assert progress.total_stages == len(CANONICAL_STAGE_KINDS)
    orch.advance()
    assert orch.progress.completed_stages == 1


@pytest.mark.parametrize("action", ACTIONS)
@pytest.mark.parametrize("student", STUDENTS[:5])
def test_action_matrix(action: str, student: str) -> None:
    orch = make_orchestrator(
        orchestrator_id=f"orch-act-{action}-{student}",
        student_id=student,
    )
    if action == "start":
        orch.start()
        assert orch.is_active()
    elif action == "advance":
        orch.start()
        done = orch.advance()
        assert done.status is StageStatus.COMPLETED
    elif action == "pause":
        orch.start()
        orch.pause("matrix-pause")
        assert orch.is_paused()
    elif action == "resume":
        orch.start()
        orch.pause("matrix-resume")
        orch.resume()
        assert orch.is_active()
    else:
        orch.start()
        advance_all_required(orch)
        orch.complete()
        assert orch.is_completed()


@pytest.mark.parametrize("strategy_type", STRATEGY_TYPES)
def test_register_episode_per_strategy(strategy_type: TeachingStrategyType) -> None:
    orch = make_orchestrator(
        orchestrator_id=f"orch-reg-{strategy_type.value}",
        strategy_type=strategy_type,
    )
    orch.start()
    episode_id = LearningEpisodeId(f"ep-{strategy_type.value}")
    orch.register_episode(episode_id)
    assert orch.has_episode(episode_id)


@pytest.mark.parametrize("status", STATUSES)
def test_status_guards_volume(status: OrchestrationStatus) -> None:
    orch = make_orchestrator(orchestrator_id=f"orch-status-{status.value}")
    if status is OrchestrationStatus.PLANNED:
        assert orch.is_planned()
        with pytest.raises(EducationalInvariantViolation):
            orch.advance()
    elif status is OrchestrationStatus.ACTIVE:
        orch.start()
        assert orch.is_active()
    elif status is OrchestrationStatus.PAUSED:
        orch.start()
        orch.pause("status-volume")
        assert orch.is_paused()
        with pytest.raises(EducationalInvariantViolation):
            orch.advance()
    else:
        orch.start()
        advance_all_required(orch)
        orch.complete()
        assert orch.is_completed()
        with pytest.raises(EducationalInvariantViolation):
            orch.resume()


@pytest.mark.parametrize("kind", STAGE_KINDS)
@pytest.mark.parametrize("point", EVIDENCE_POINTS)
def test_stage_kind_evidence_point_pairing(
    kind: OrchestrationStageKind, point: EvidenceCollectionPointKind
) -> None:
    if kind is OrchestrationStageKind.EVIDENCE_COLLECTION:
        stage = make_stage(
            stage_id=f"pair-{kind.value}-{point.value}",
            kind=kind,
            evidence_collection_point=point,
        )
        assert stage.evidence_collection_point is point
    else:
        stage = make_stage(
            stage_id=f"pair-{kind.value}-{point.value}",
            kind=kind,
            evidence_collection_point=point,
        )
        assert stage.is_evidence_collection_point()


@pytest.mark.parametrize("strategy_type", STRATEGY_TYPES)
@pytest.mark.parametrize("point", EVIDENCE_POINTS)
def test_strategy_evidence_point_create(
    strategy_type: TeachingStrategyType, point: EvidenceCollectionPointKind
) -> None:
    stages = [
        make_stage(
            stage_id="ev-only",
            kind=OrchestrationStageKind.EVIDENCE_COLLECTION,
            sequence_index=0,
            evidence_collection_point=point,
        )
    ]
    orch = make_orchestrator(
        orchestrator_id=f"orch-sep-{strategy_type.value}-{point.value}",
        strategy_type=strategy_type,
        plan=make_plan(stages=stages),
    )
    assert OrchestrationIsValidSpecification().is_satisfied_by(orch)
    orch.start()
    orch.advance()
    orch.complete()
    assert orch.is_completed()


@pytest.mark.parametrize("student", STUDENTS)
@pytest.mark.parametrize("point", EVIDENCE_POINTS)
def test_student_evidence_point_lifecycle(
    student: str, point: EvidenceCollectionPointKind
) -> None:
    stages = [
        make_stage(
            stage_id="c",
            kind=OrchestrationStageKind.EPISODE_CREATION,
            sequence_index=0,
        ),
        make_stage(
            stage_id="e",
            kind=OrchestrationStageKind.EVIDENCE_COLLECTION,
            sequence_index=1,
            evidence_collection_point=point,
        ),
        make_stage(
            stage_id="r",
            kind=OrchestrationStageKind.REFLECTION,
            sequence_index=2,
        ),
    ]
    orch = make_orchestrator(
        orchestrator_id=f"orch-sep2-{student}-{point.value}",
        student_id=student,
        plan=make_plan(stages=stages),
    )
    orch.start()
    while not orch.progress.all_stages_complete:
        orch.advance()
    orch.complete()
    assert orch.progress.evidence_points_complete


@pytest.mark.parametrize("strategy_a", STRATEGY_TYPES)
@pytest.mark.parametrize("strategy_b", STRATEGY_TYPES)
def test_multi_strategy_references(
    strategy_a: TeachingStrategyType, strategy_b: TeachingStrategyType
) -> None:
    if strategy_a is strategy_b:
        refs = [make_strategy_ref(strategy_type=strategy_a)]
    else:
        refs = [
            make_strategy_ref(
                strategy_id=f"sa-{strategy_a.value}",
                strategy_type=strategy_a,
            ),
            make_strategy_ref(
                strategy_id=f"sb-{strategy_b.value}",
                strategy_type=strategy_b,
            ),
        ]
    orch = make_orchestrator(
        orchestrator_id=f"orch-ms-{strategy_a.value}-{strategy_b.value}",
        strategy_references=refs,
    )
    assert orch.strategy_count() == len(refs)
    assert OrchestrationIsValidSpecification().is_satisfied_by(orch)


@pytest.mark.parametrize("kind", STAGE_KINDS)
def test_cannot_complete_mid_kind(kind: OrchestrationStageKind) -> None:
    orch = make_started_orchestrator(
        orchestrator_id=f"orch-mid-{kind.value}",
    )
    # Advance at most once so required sequence remains incomplete.
    orch.advance()
    if orch.progress.required_sequence_complete:
        pytest.skip("single advance completed all required")
    with pytest.raises(EducationalInvariantViolation):
        orch.complete()
